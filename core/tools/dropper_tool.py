from core.tools.drawing_tool import DrawingTool
from PyQt6.QtGui import QColor


class DropperTool(DrawingTool):
    def __init__(self, canvas):
        super().__init__(canvas)

    def get_tool_name(self) -> str:
        return 'dropper'

    # def start_drawing(self, point):
    #     image = self.canvas.grabFramebuffer()
        
    #     x = int(point.x())
    #     y = int(point.y())
        
    #     # หากสี ไม่ตรง ลองเซ็ก Y-axis
    #     # y = image.height() - int(point.y())
        
    #     if x < 0 or y < 0 or x >= image.width() or y >= image.height():
    #         return
        
    #     color = QColor(image.pixel(x, y))
        
    #     r = color.red()
    #     g = color.green()
    #     b = color.blue()
        
    #     self.canvas.current_color = (r, g, b)
    #     print(f"Picked color: {r}, {g}, {b}")
    #     print(f"Point clicked: {point.x()}, {point.y()}")
    #     print(f"Image size: {image.width()} x {image.height()}")
    #     print(f"Canvas size: {self.canvas.width()} x {self.canvas.height()}")
    #     print(f"Pixel color before: {color.getRgb()}")

    def start_drawing(self, point):
        image = self.canvas.grabFramebuffer()
        
        scale_x = image.width() / self.canvas.width()
        scale_y = image.height() / self.canvas.height()
        
        x = int(point.x() * scale_x)
        y = int(point.y() * scale_y)
        
        if x < 0 or y < 0 or x >= image.width() or y >= image.height():
            return
        
        color = QColor(image.pixel(x, y))
        r = color.red() / 255.0
        g = color.green() / 255.0
        b = color.blue() / 255.0
        
        picked_color = (r, g, b)
            
        self.canvas.current_color = picked_color
        self.canvas.on_color_changed(picked_color)
        
        print(f"Picked color: {r}, {g}, {b}")
        print(f"Point clicked: {point.x()}, {point.y()}")
        print(f"Image size: {image.width()} x {image.height()}")
        print(f"Canvas size: {self.canvas.width()} x {self.canvas.height()}")
        print(f"Pixel color before: {color.getRgb()}")

    def continue_drawing(self, point):
        pass

    def finish_drawing(self, point):
        pass

    def render(self, color: tuple, width: int) -> None:
        return super().render(color, width)