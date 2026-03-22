from PyQt6.QtOpenGLWidgets import QOpenGLWidget
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

# เดี๋ยวนำเข้า Tool อื่นๆ เพิ่มตรงนี้เมื่อสร้างเสร็จ
from core.tools.line_tool import LineTool 
from core.tools.pen_tool import PenTool
from core.tools.eraser_tool import EraserTool
from core.tools.dropper_tool import DropperTool
from core.tools.rectangle_tool import RectangleTool
from core.tools.circle_tool import CircleTool
from core.tools.triangle_tool import TriangleTool

class CanvasPanel(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.current_color = (0, 0, 0) # สีดำเริ่มต้น
        self.current_width = 2
        
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
        """เรนเดอร์ข้อมูลพิกเซลทั้งหมดที่ถูกบันทึกไว้ในประวัติแบบรวดเร็ว (Batch Rendering)"""
        
        # เปิดใช้งานโหมดอ่านข้อมูลจาก Array
        glEnableClientState(GL_VERTEX_ARRAY)
        
        for item in self.history:
            glColor3f(*item['color'])
            glPointSize(item['width'])
            
            data = item['data']
            if len(data) == 0:
                continue
                
            if not isinstance(data, np.ndarray):
                data = np.array(data, dtype=np.float32)
                item['data'] = data
                
            # ชี้เป้าให้ OpenGL อ่านข้อมูลจาก Numpy array ทันที
            glVertexPointer(2, GL_FLOAT, 0, data)
            # สั่งวาดรวดเดียวจบตามจำนวนข้อมูล
            glDrawArrays(GL_POINTS, 0, len(data))
            
        # ปิดการใช้งานเมื่อวาดเสร็จ
        glDisableClientState(GL_VERTEX_ARRAY)
        
    def setup_tools(self):
        self.tools = {
            'pen': PenTool(self),
            'fill': None,
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
            
    def get_pixel_color(self, x: int, y: int) -> tuple:
        """อ่านค่าสีของพิกเซลจากหน้าจอโดยตรง ไม่ต้องวนลูปหาในประวัติ"""
        canvas_array = self.get_canvas_array()
        
        # ตรวจสอบว่าพิกัดที่เมาส์ชี้ อยู่ในขอบเขตหน้าจอหรือไม่
        h, w = canvas_array.shape[:2]
        if 0 <= x < w and 0 <= y < h:
            # ดึงสี RGB ออกมา (0-255)
            r, g, b = canvas_array[y, x]
            # OpenGL ในโปรแกรมคุณเก็บสีเป็น 0.0 - 1.0 เราต้องหาร 255.0
            return (r / 255.0, g / 255.0, b / 255.0)
            
        return (1.0, 1.0, 1.0)  # พื้นหลังสีขาว

    def get_canvas_size(self) -> tuple:
        """คืนขนาดของ canvas"""
        return (self.width(), self.height())
    
    def get_canvas_array(self) -> np.ndarray:
        """ดึงภาพ Canvas ปัจจุบันออกมาเป็น Numpy Array เพื่อให้ประมวลผลได้เร็วสุดขีด"""
        # grabFramebuffer() ของ PyQt จะดึงภาพหน้าจอ OpenGL ปัจจุบันออกมาเป็น QImage
        qimage = self.grabFramebuffer()
        
        # ดึงข้อมูลดิบและแปลงเป็น Numpy Array (ความสูง, ความกว้าง, 4 ช่องสี RGBA)
        ptr = qimage.bits()
        ptr.setsize(qimage.sizeInBytes())
        
        # ปกติภาพที่ได้จะเป็น Format ที่มี 4 channels (RGBA หรือ BGRA ขึ้นอยู่กับระบบ)
        arr = np.array(ptr, dtype=np.uint8).reshape(qimage.height(), qimage.width(), 4)
        
        # คืนค่าเป็น Array (สมมติว่าเอาแค่ RGB ตัด Alpha ทิ้ง)
        return arr[:, :, :3]
            
    # ==========================================
    # -- จัดการ Mouse Events --    
    # ==========================================
    def mousePressEvent(self, event):
        if self.current_tool:
            self.current_tool.start_drawing(event.position())
            drawn_data = self.current_tool.start_drawing(event.position())
            
            if drawn_data is not None and len(drawn_data) > 0:
                self.history.append({
                    'tool_name': self.current_tool.get_tool_name(),
                    'color': self.current_color,
                    'width': self.current_width,
                    'data': drawn_data
                })
                
            self.update() # สั่งให้ paintGL ทำงานเพื่อวาดจุดเริ่มต้น

    def mouseMoveEvent(self, event):
        # ทำงานเฉพาะตอนที่กดเมาส์ค้างไว้ (is_drawing = True)
        if self.current_tool and getattr(self.current_tool, 'is_drawing', False):
            self.current_tool.continue_drawing(event.position())
            self.update() # สั่งให้ paintGL อัปเดตภาพพรีวิวตามเมาส์

    def mouseReleaseEvent(self, event):
        if self.current_tool and getattr(self.current_tool, 'is_drawing', False):
            drawn_data = self.current_tool.finish_drawing(event.position())
            
            if drawn_data is not None and len(drawn_data) > 0:
                # แปลงร่างเป็น Numpy Array ชนิด Float32 ทันที! เพื่อให้พร้อมส่งเข้าการ์ดจอ
                optimized_data = np.array(drawn_data, dtype=np.float32)
                
                color = self.current_color
                
                if self.current_tool.get_tool_name() == 'eraser':
                    color = (1.0, 1.0, 1.0)  # สีขาวสำหรับลบ
                    
                self.history.append({
                    'tool_name': self.current_tool.get_tool_name(),
                    'color': color,
                    'width': self.current_width,
                    'data': optimized_data  # เก็บแบบ Array แทน
                })
            
            self.update()