from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *

# เดี๋ยวนำเข้า Tool อื่นๆ เพิ่มตรงนี้เมื่อสร้างเสร็จ
from core.tools.line_tool import LineTool 
from core.tools.pen_tool import PenTool
from core.tools.fill_tool import FillTool
from core.tools.eraser_tool import EraserTool
from core.tools.dropper_tool import DropperTool
from core.tools.rectangle_tool import RectangleTool
from core.tools.circle_tool import CircleTool
from core.tools.triangle_tool import TriangleTool

class CanvasPanel(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.current_color = (0, 0, 0) # สีดำเริ่มต้น
        self.current_width = 1
        
        # ระบบ History: เก็บประวัติการวาดที่เสร็จสมบูรณ์แล้วทั้งหมด
        # รูปแบบ: [{'tool_name': 'line', 'color': (0,0,0), 'width': 1, 'data': [(x,y), (x,y), ...]}]
        self.history = [] 
        
        self.tools = {}
        self.current_tool = None
        self.setup_tools()
        
    def initializeGL(self):
        glClearColor(1.0, 1.0, 1.0, 1.0) # พื้นหลังสีขาว
        
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        # ตั้งค่าให้ (0,0) อยู่มุมซ้ายบน และ (width, height) อยู่มุมขวาล่าง
        glOrtho(0, width, height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        
        # 1. วาดสิ่งที่เคยวาดเสร็จไปแล้ว (History)
        self.draw_history()
        
        # 2. วาดภาพพรีวิวของ Tool ปัจจุบัน (ขณะกำลังลากเมาส์)
        if self.current_tool and getattr(self.current_tool, 'is_drawing', False):
            self.current_tool.render(self.current_color, self.current_width)
            
    def draw_history(self):
        """เรนเดอร์ข้อมูลพิกเซลทั้งหมดที่ถูกบันทึกไว้ในประวัติ"""
        for item in self.history:
            # ตั้งค่าสี (ต้องแปลงจาก 0-255 เป็น 0.0-1.0 สำหรับ OpenGL)
 
            glColor3f(*item['color'])
            
            # ตั้งค่าขนาดจุด (ความหนาของเส้น)
            glPointSize(item['width'])
            
            # วาดจุดทั้งหมดที่ได้จาก Algorithm
            if item['data']:
                glBegin(GL_POINTS)
                for x, y in item['data']:
                    glVertex2f(x, y)
                glEnd()
        
    def setup_tools(self):
        self.tools = {
            'pen': PenTool(self),
            'fill': FillTool(self),
            'eraser': EraserTool(self),
            'dropper': DropperTool(self),
            'line': LineTool(self), 
            'rectangle': RectangleTool(self),
            'circle': CircleTool(self),
            'triangle': TriangleTool(self),
            # เพิ่ม tools อื่นๆ ทีหลัง
        }
        self.current_tool = self.tools.get('pen')
        
    def on_color_changed(self, color):
        """Handle color change from color picker"""
        # เปลี่ยน tuple (r,g,b) เป็น (0-255)
        self.current_color = color
        
    def on_tool_selected(self, tool_name: str):
        """Handle tool selection from tool panel"""
        self.set_tool(tool_name) 
    
    def set_tool(self, tool_name: str):
        # ปลดล็อกเงื่อนไข เพื่อให้สามารถสลับ Tool ได้จริง
        if tool_name in self.tools:
            self.current_tool = self.tools[tool_name]
            print(f"Canvas: Changed tool to {tool_name}")
        else:
            print(f"Canvas: Tool '{tool_name}' ยังไม่ได้ถูกสร้างหรือลงทะเบียน")
            self.current_tool = None
            
    # ==========================================
    # -- จัดการ Mouse Events --    
    # ==========================================
    def mousePressEvent(self, event):
        if self.current_tool:
            self.current_tool.start_drawing(event.position())
            self.update() # สั่งให้ paintGL ทำงานเพื่อวาดจุดเริ่มต้น

    def mouseMoveEvent(self, event):
        # ทำงานเฉพาะตอนที่กดเมาส์ค้างไว้ (is_drawing = True)
        if self.current_tool and getattr(self.current_tool, 'is_drawing', False):
            self.current_tool.continue_drawing(event.position())
            self.update() # สั่งให้ paintGL อัปเดตภาพพรีวิวตามเมาส์

    def mouseReleaseEvent(self, event):
        if self.current_tool and getattr(self.current_tool, 'is_drawing', False):
            # 1. รับข้อมูลกลุ่มพิกเซลจากการคำนวณของ Algorithm เมื่อวาดเสร็จ
            drawn_data = self.current_tool.finish_drawing(event.position())
            
            # 2. ถ้ายกเมาส์แล้วมีข้อมูล (เช่น ลากเส้นเสร็จแล้ว) ให้บันทึกลง History
            if drawn_data is not None and len(drawn_data) > 0:
                self.history.append({
                    'tool_name': self.current_tool.get_tool_name(),
                    'color': self.current_color,
                    'width': self.current_width,
                    'data': drawn_data
                })
            
            # 3. อัปเดตหน้าจอเพื่อย้ายจากการวาด Preview ไปวาดจาก History
            self.update()