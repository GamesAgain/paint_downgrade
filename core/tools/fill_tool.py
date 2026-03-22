import numpy as np
from typing import List, Tuple, Optional
from collections import deque
from PyQt6.QtCore import QPointF

from .drawing_tool import DrawingTool


class FillTool(DrawingTool):
    def __init__(self, canvas):
        super().__init__(canvas)

    def get_tool_name(self) -> str:
        return 'fill'

    # ขยายขอบเส้นให้หนาขึ้นใน mask เพื่อไม่ให้ fill ทับเส้น
    def expand_mask(self, mask):
        h, w = mask.shape
        new_mask = mask.copy()

        for y in range(1, h - 1):
            for x in range(1, w - 1):
                if mask[y, x]:
                    # ขยายออก 4 ทิศ และจุดตรงกลาง
                    for dy, dx in [(0,0), (1,0), (-1,0), (0,1), (0,-1)]:
                        new_mask[y + dy, x + dx] = True

        return new_mask

    def start_drawing(self, point: QPointF, modifiers=None) -> Optional[List[Tuple[float, float]]]:
        x = int(point.x())
        y = int(point.y())

        width = self.canvas.width()
        height = self.canvas.height()

        # ถ้าคลิกนอกพื้นที่ ไม่ทำงาน
        if x < 0 or x >= width or y < 0 or y >= height:
            return None

        # สร้างภาพพื้นหลังสีขาว
        img = np.full((height, width, 3), 255, dtype=np.uint8)

        # สร้าง mask สำหรับเก็บตำแหน่งของเส้น
        line_mask = np.zeros((height, width), dtype=bool)

        # วาดข้อมูลจาก history ลงในภาพ
        for item in self.canvas.history:
            color = item['color']
            color255 = (np.array(color) * 255).astype(np.uint8)

            for px, py in item['data']:
                xi, yi = int(px), int(py)
                if 0 <= xi < width and 0 <= yi < height:
                    img[yi, xi] = color255

                    # ถ้าเป็นเครื่องมือวาดเส้น ให้บันทึกลง mask
                    if item['tool_name'] in ['pen', 'line', 'rectangle', 'circle']:
                        line_mask[yi, xi] = True

        # ขยาย mask เพื่อให้เส้นหนาขึ้น
        line_mask = self.expand_mask(line_mask)

        # สีที่ต้องการแทนที่
        target_color = img[y, x].copy()

        # สีที่ใช้เติม
        fill_color = (np.array(self.canvas.current_color) * 255).astype(np.uint8)

        return self.flood_fill_numpy(img, line_mask, x, y, target_color, fill_color)

    def continue_drawing(self, point, modifiers=None):
        pass

    def finish_drawing(self, point, modifiers=None):
        pass

    # flood fill แบบ BFS
    def flood_fill_numpy(self, img, line_mask, sx, sy, target_color, fill_color):
        height, width, _ = img.shape

        # ใช้ queue สำหรับการกระจาย
        queue = deque([(sx, sy)])

        # ใช้เก็บจุดที่เคยตรวจแล้ว
        visited = np.zeros((height, width), dtype=bool)

        filled = []

        # ตรวจว่าสีใกล้เคียงกันหรือไม่
        def is_similar(c1, c2, tol=40):
            return abs(int(c1[0]) - int(c2[0])) + \
                   abs(int(c1[1]) - int(c2[1])) + \
                   abs(int(c1[2]) - int(c2[2])) < tol

        while queue:
            x, y = queue.popleft()

            # ข้ามถ้าอยู่นอกภาพ
            if x < 0 or x >= width or y < 0 or y >= height:
                continue

            # ข้ามถ้าเคยตรวจแล้ว
            if visited[y, x]:
                continue
            visited[y, x] = True

            # ข้ามถ้าเป็นเส้น
            if line_mask[y, x]:
                continue

            pixel = img[y, x]

            # ข้ามถ้าสีไม่ใกล้เคียงกับจุดเริ่มต้น
            if not is_similar(pixel, target_color):
                continue

            # เปลี่ยนสี
            img[y, x] = fill_color
            filled.append((float(x), float(y)))

            # เพิ่มเพื่อนบ้าน 4 ทิศ
            queue.append((x + 1, y))
            queue.append((x - 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))

        return filled

    def render(self, color: tuple, width: int) -> None:
        pass