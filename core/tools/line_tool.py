from typing import List, Tuple, Optional
from PyQt6.QtCore import QPointF
from OpenGL.GL import *

from core.tools.drawing_tool import DrawingTool

class LineTool(DrawingTool):
    """
    เครื่องมือวาดเส้นตรง (Straight Line)
    ทำงานเหมือน Paint: คลิกจุดเริ่มต้น -> ลากเพื่อดูพรีวิว -> ปล่อยเพื่อวาดเส้นตรง
    ใช้ Bresenham's Algorithm จากคลาสแม่ในการคำนวณพิกเซล
    """
    def __init__(self, canvas):
        super().__init__(canvas)
        self.current_point: Optional[QPointF] = None

    def get_tool_name(self) -> str:
        return 'line'

    def start_drawing(self, point: QPointF, modifiers=None) -> None:
        """เริ่มวาด: บันทึกจุดเริ่มต้นของเส้น"""
        self.is_drawing = True
        self.start_point = point
        self.current_point = point

    def continue_drawing(self, point: QPointF, modifiers=None) -> None:
        """อัปเดตพรีวิว: อัปเดตจุดปัจจุบันเพื่อแสดงเส้นพรีวิว"""
        if not self.is_drawing or self.start_point is None:
            return
        self.current_point = point

    def finish_drawing(self, point: QPointF, modifiers=None) -> Optional[List[Tuple[float, float]]]:
        """จบการวาด: คำนวณเส้นตรงสุดท้ายและส่งข้อมูลพิกเซล"""
        if not self.is_drawing or self.start_point is None:
            return None
            
        # คำนวณพิกเซลทั้งหมดบนเส้นตรงจากจุดเริ่มต้นถึงจุดสุดท้าย
        line_points = self.calculate_bresenham(self.start_point, point)
        
        # รีเซ็ตสถานะ
        self.is_drawing = False
        self.start_point = None
        self.current_point = None
        
        # ส่งข้อมูลพิกเซลทั้งหมดให้ Canvas บันทึกลง History
        return line_points

    def render(self, color: tuple, width: int) -> None:
        """เรนเดอร์พรีวิว: วาดเส้นตรงจากจุดเริ่มต้นถึงจุดปัจจุบัน"""
        if not self.is_drawing or self.start_point is None or self.current_point is None:
            return
            
        # คำนวณพิกเซลสำหรับเส้นพรีวิว
        preview_points = self.calculate_bresenham(self.start_point, self.current_point)
        
        # ตั้งค่าสีและความหนา
        glColor3f(*color)
        glPointSize(width)
        
        # วาดพิกเซลทั้งหมดของเส้นพรีวิว
        glBegin(GL_POINTS)
        for x, y in preview_points:
            glVertex2f(x, y)
        glEnd()