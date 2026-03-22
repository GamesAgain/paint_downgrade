from typing import List, Tuple, Optional
from PyQt6.QtCore import QPointF
from OpenGL.GL import *

from core.tools.drawing_tool import DrawingTool

class PenTool(DrawingTool):
    """
    เครื่องมือวาดเส้นอิสระ (Continuous Drawing)
    บันทึกทุกจุดที่เมาส์ลากผ่าน และใช้ Bresenham เพื่อถมช่องว่างกรณีที่ลากเมาส์เร็วเกินไป
    """
    def __init__(self, canvas):
        super().__init__(canvas)
        self.last_point: Optional[QPointF] = None
        self.stroke_points: List[Tuple[float, float]] = []

    def get_tool_name(self) -> str:
        return 'pen'

    def start_drawing(self, point: QPointF, modifiers=None) -> None:
        """เริ่มวาด: รีเซ็ตเส้นใหม่และเก็บจุดแรก"""
        self.is_drawing = True
        self.stroke_points = [] # เคลียร์ข้อมูลพิกเซลของเส้นเก่า
        self.last_point = point
        
        # เก็บจุดเริ่มต้นลงไปใน List
        self.stroke_points.append((float(int(point.x())), float(int(point.y()))))

    def continue_drawing(self, point: QPointF, modifiers=None) -> None:
        """วาดต่อ: ลากเมาส์ไปเรื่อยๆ เติมเต็มช่องว่างด้วย Bresenham"""
        if not self.is_drawing or self.last_point is None:
            return
        # ใช้ Bresenham หาพิกเซลทั้งหมดระหว่างจุดก่อนหน้า กับ จุดปัจจุบัน
        new_points = self.calculate_bresenham(self.last_point, point)
        
        # นำจุดที่ได้มาต่อท้ายใน List ของเส้นนี้ (ข้ามจุดแรกของ segment เพื่อไม่ให้ซ้ำซ้อน)
        if len(new_points) > 1:
            self.stroke_points.extend(new_points[1:])
            
        # อัปเดตจุดล่าสุด
        self.last_point = point

    def finish_drawing(self, point: QPointF, modifiers=None) -> Optional[List[Tuple[float, float]]]:
        """จบการวาด: วาด segment สุดท้ายและส่งข้อมูลให้ Canvas"""
        if not self.is_drawing or self.last_point is None:
            return None
            
        # เติมเส้นส่วนสุดท้าย
        new_points = self.calculate_bresenham(self.last_point, point)
        if len(new_points) > 1:
            self.stroke_points.extend(new_points[1:])
            
        self.is_drawing = False
        self.last_point = None
        
        # ส่ง List พิกเซลทั้งหมดของเส้นนี้ไปให้ Canvas บันทึกลง History
        return self.stroke_points

    def render(self, color: tuple, width: int) -> None:
        """เรนเดอร์: วาดจุดทั้งหมดที่เก็บสะสมไว้ใน stroke_points"""
        if not self.is_drawing or not self.stroke_points:
            return
            
        # ตั้งค่าสี
        
        glColor3f(*color)
        
        # ตั้งค่าความหนาของเส้น
        glPointSize(width)
        
        # วาดพิกเซลทั้งหมดที่มี ณ ตอนนั้น
        glBegin(GL_POINTS)
        for x, y in self.stroke_points:
            glVertex2f(x, y)
        glEnd()