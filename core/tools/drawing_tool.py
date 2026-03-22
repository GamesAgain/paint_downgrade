from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Any
from PyQt6.QtCore import QPointF
from PyQt6.QtCore import Qt

class DrawingTool(ABC):
    """
    คลาสแม่ (Abstract Base Class) สำหรับเครื่องมือวาดภาพทุกชนิด
    เครื่องมือทุกตัวจะต้องสืบทอด (Inherit) จากคลาสนี้และเขียนการทำงานของเมธอดต่างๆ ให้ครบถ้วน
    """
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.is_drawing = False
        self.start_point: Optional[QPointF] = None
    
    @abstractmethod
    def start_drawing(self, point: QPointF, modifiers=None) -> None:
        """
        ทำงานเมื่อ: ผู้ใช้ 'คลิกเมาส์ครั้งแรก' ลงบน Canvas
        หน้าที่หลัก: 
        - บันทึกจุดเริ่มต้น (เช่น self.start_point = point)
        - เปลี่ยนสถานะการวาด (self.is_drawing = True)
        """
        pass
    
    @abstractmethod
    def continue_drawing(self, point: QPointF, modifiers=None) -> None:
        """
        ทำงานเมื่อ: ผู้ใช้ 'กดเมาส์ค้างแล้วลาก' ไปมาบน Canvas
        หน้าที่หลัก:
        - อัปเดตพิกัดเป้าหมายชั่วคราว (เช่น self.current_point = point)
        - เพื่อให้เมธอด render() นำพิกัดนี้ไปคำนวณและวาดภาพพรีวิว (Preview) แบบ Real-time
        """
        pass
    
    @abstractmethod
    def finish_drawing(self, point: QPointF, modifiers=None) -> Optional[Any]:
        """
        ทำงานเมื่อ: ผู้ใช้ 'ปล่อยคลิกเมาส์'
        หน้าที่หลัก:
        - คำนวณผลลัพธ์พิกเซลแบบสมบูรณ์เป็นครั้งสุดท้าย
        - ปรับสถานะหยุดวาด (self.is_drawing = False) และรีเซ็ตค่าพิกัด
        - **สำคัญมาก:** ต้องส่งคืน (Return) ข้อมูลพิกัดทั้งหมด (เช่น List ของ X,Y) 
          กลับไปให้ Canvas บันทึกลงประวัติ (History) หากไม่มีข้อมูลให้คืนค่า None
        """
        pass
    
    @abstractmethod
    def get_tool_name(self) -> str:
        """
        หน้าที่หลัก: คืนค่าชื่อของเครื่องมือ (String) เช่น 'pen', 'line', 'rectangle'
        เพื่อใช้ระบุใน History ของ Canvas ว่าชุดพิกเซลนี้ถูกวาดด้วยเครื่องมืออะไร
        """
        pass

    @abstractmethod
    def render(self, color: tuple, width: int) -> None:
        """
        ทำงานเมื่อ: กำลังลากเมาส์วาด (ถูกเรียกใช้โดย paintGL ของ Canvas)
        หน้าที่หลัก: 
        - แสดงผลภาพพรีวิวบางๆ ให้ผู้ใช้เห็นก่อนที่จะปล่อยเมาส์ 
        - ต้องใช้คำสั่งของ OpenGL (เช่น glBegin, glVertex2f) ในการวาดพิกเซล
        - รับค่า color (สี) และ width (ความหนา) ที่แปลงมาให้พร้อมใช้แล้วจาก Canvas
        """
        pass

    # ==========================================
    # Utility Algorithms (เครื่องมือส่วนกลาง)
    # ==========================================
    def calculate_bresenham(self, p1: QPointF, p2: QPointF) -> List[Tuple[float, float]]:
        """
        ฟังก์ชันคำนวณพิกเซลบนเส้นตรงด้วย Bresenham's Algorithm
        จัดเตรียมไว้ให้คลาสลูกๆ (เช่น Line, Pen, Rectangle, Triangle) เรียกใช้ได้ทันที 
        (เช่น เรียกผ่าน self.calculate_bresenham) โดยไม่ต้องเขียนโค้ดนี้ซ้ำอีก
        """
        points = []
        x1, y1 = int(p1.x()), int(p1.y())
        x2, y2 = int(p2.x()), int(p2.y())
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        while True:
            points.append((float(x1), float(y1)))
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
                
        return points