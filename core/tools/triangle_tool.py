from typing import List, Tuple, Optional, Set
from PyQt6.QtCore import QPointF
from OpenGL.GL import *
import math
from collections import deque

from core.tools.drawing_tool import DrawingTool

class TriangleTool(DrawingTool):
    """
    เครื่องมือวาดสามเหลี่ยม
    ผู้ใช้ดำเนินการ: คลิกและลากเมาส์เพื่อวาดสามเหลี่ยม
    สามเหลี่ยมจะมี 2 จุดมาจากการลาก และจุดที่ 3 คำนวณจากเวกเตอร์ตั้งฉาก
    """
    def __init__(self, canvas):
        super().__init__(canvas)
        self.current_point: Optional[QPointF] = None
        self.triangle_points: List[Tuple[float, float]] = []

    def get_tool_name(self) -> str:
        return 'triangle'

    def start_drawing(self, point: QPointF, modifiers=None) -> None:
        """เริ่มวาด: บันทึกจุดเริ่มต้น"""
        self.is_drawing = True
        self.start_point = point
        self.current_point = point
        self.triangle_points = []

    def continue_drawing(self, point: QPointF, modifiers=None) -> None:
        """ยังคงวาด: อัปเดตจุดปัจจุบันขณะลากเมาส์"""
        if not self.is_drawing:
            return
        self.current_point = point

    def finish_drawing(self, point: QPointF, modifiers=None) -> Optional[List[Tuple[float, float]]]:
        """จบการวาด: คำนวณ 3 จุดของสามเหลี่ยม และวาดขอบเท่านั้น (ไม่มี fill)"""
        if not self.is_drawing or self.start_point is None or self.current_point is None:
            return None

        # คำนวณจุดทั้ง 3 ของสามเหลี่ยม
        p1 = self.start_point
        p2 = point
        p3 = self._calculate_third_vertex(p1, p2)

        # วาด 3 เส้นเชื่อมจุด (ขอบ)
        all_points: List[Tuple[float, float]] = []

        # เส้นที่ 1: p1 -> p2
        line1 = self.calculate_bresenham(p1, p2)
        all_points.extend(line1)

        # เส้นที่ 2: p2 -> p3
        line2 = self.calculate_bresenham(p2, p3)
        if len(line2) > 1:
            all_points.extend(line2[1:])  # ข้ามจุดแรกเพื่อไม่ให้ซ้ำซ้อน

        # เส้นที่ 3: p3 -> p1
        line3 = self.calculate_bresenham(p3, p1)
        if len(line3) > 1:
            all_points.extend(line3[1:])  # ข้ามจุดแรกเพื่อไม่ให้ซ้ำซ้อน

        self.is_drawing = False
        self.start_point = None
        self.current_point = None

        return all_points

    def _calculate_third_vertex(self, p1: QPointF, p2: QPointF) -> QPointF:
        """
        คำนวณจุดที่ 3 ของสามเหลี่ยม
        จุดที่ 3 จะอยู่ที่ตำแหน่งตั้งฉากกับเส้น p1-p2
        เพื่อให้สามเหลี่ยมมีรูปร่างสวยงาม
        """
        # คำนวณจุดกึ่งกลางของ p1 และ p2 (เป็นฐาน)
        mid_x = (p1.x() + p2.x()) / 2
        mid_y = (p1.y() + p2.y()) / 2

        # คำนวณความยาวของฐาน
        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()
        base_length = math.sqrt(dx * dx + dy * dy)

        # คำนวณความสูงของสามเหลี่ยม (ใช้ 0.866 สำหรับสามเหลี่ยมเท่า)
        height = base_length * 0.866

        # เวกเตอร์ตั้งฉากกับฐาน (หมุน 90 องศา)
        if base_length > 0:
            perp_x = -dy / base_length
            perp_y = dx / base_length
        else:
            perp_x = 0
            perp_y = 1

        # จุดที่ 3: จุดกึ่งกลาง + เวกเตอร์ตั้งฉาก * ความสูง
        p3_x = mid_x + perp_x * height
        p3_y = mid_y + perp_y * height

        return QPointF(p3_x, p3_y)

    def _fill_triangle(self, p1: QPointF, p2: QPointF, p3: QPointF) -> List[Tuple[float, float]]:
        """
        เติมสีภายในสามเหลี่ยม ใช้ Flood Fill Algorithm (เหมือน Paint program)
        1. เริ่มจากจุดศูนย์กลางของสามเหลี่ยม
        2. ใช้ BFS เพื่อกระจายการเติมสีไปยัง pixel ที่อยู่ติดกัน
        """
        fill_points: List[Tuple[float, float]] = []
        
        # หาจุดศูนย์กลางของสามเหลี่ยม (เป็นจุด Seed)
        center_x = (p1.x() + p2.x() + p3.x()) / 3
        center_y = (p1.y() + p2.y() + p3.y()) / 3
        
        seed_x = int(center_x)
        seed_y = int(center_y)
        
        # ใช้ Flood Fill algorithm (BFS - Breadth-First Search)
        visited: Set[Tuple[int, int]] = set()
        queue: deque = deque([(seed_x, seed_y)])
        visited.add((seed_x, seed_y))
        
        # ขอบเขต
        min_x = int(min(p1.x(), p2.x(), p3.x())) - 1
        max_x = int(max(p1.x(), p2.x(), p3.x())) + 1
        min_y = int(min(p1.y(), p2.y(), p3.y())) - 1
        max_y = int(max(p1.y(), p2.y(), p3.y())) + 1
        
        while queue:
            x, y = queue.popleft()
            
            # ตรวจสอบว่า (x, y) อยู่ในสามเหลี่ยมหรือไม่
            if not self._point_in_triangle(x, y, p1, p2, p3):
                continue
            
            # เพิ่มจุดนี้เข้า fill_points
            fill_points.append((float(x), float(y)))
            
            # ตรวจสอบ 4 ทิศทาง (Up, Down, Left, Right) - 4-way connectivity
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                
                # ตรวจสอบขอบเขต
                if min_x <= nx <= max_x and min_y <= ny <= max_y:
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
        
        return fill_points

    def _point_in_triangle(self, x: float, y: float, p1: QPointF, p2: QPointF, p3: QPointF) -> bool:
        """
        ตรวจสอบว่าจุด (x, y) อยู่ในสามเหลี่ยมหรือไม่
        ใช้ Barycentric coordinates method
        """
        # แปลงจุด QPointF เป็นค่าตัวเลข
        x1, y1 = p1.x(), p1.y()
        x2, y2 = p2.x(), p2.y()
        x3, y3 = p3.x(), p3.y()

        # คำนวณพื้นที่ของสามเหลี่ยมหลัก
        area = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))

        if area < 1e-6:  # สามเหลี่ยมเสื่อม (ความพื้นที่ต่ำสุด)
            return False

        # คำนวณพื้นที่ของสามเหลี่ยมย่อย 3 อัน
        area1 = abs((x - x2) * (y3 - y2) - (x3 - x2) * (y - y2))
        area2 = abs((x1 - x) * (y3 - y) - (x3 - x) * (y1 - y))
        area3 = abs((x1 - x2) * (y - y2) - (x - x2) * (y1 - y2))

        # ถ้าผลรวมพื้นที่ย่อย ≈ พื้นที่หลัก แสดงว่าจุดอยู่ในสามเหลี่ยม
        return abs(area1 + area2 + area3 - area) < 1

    def render(self, color: tuple, width: int) -> None:
        """เรนเดอร์: วาดเฉพาะขอบสามเหลี่ยมเท่านั้น (ไม่มี fill ตอนลาก)"""
        if not self.is_drawing or self.start_point is None or self.current_point is None:
            return

        # คำนวณจุดทั้ง 3
        p1 = self.start_point
        p2 = self.current_point
        p3 = self._calculate_third_vertex(p1, p2)

        # วาดเฉพาะขอบ (ไม่มี fill preview)
        glColor3f(*color)
        glPointSize(width)
        glBegin(GL_POINTS)

        # เส้นที่ 1: p1 -> p2
        for x, y in self.calculate_bresenham(p1, p2):
            glVertex2f(x, y)

        # เส้นที่ 2: p2 -> p3
        for x, y in self.calculate_bresenham(p2, p3):
            glVertex2f(x, y)

        # เส้นที่ 3: p3 -> p1
        for x, y in self.calculate_bresenham(p3, p1):
            glVertex2f(x, y)

        glEnd()