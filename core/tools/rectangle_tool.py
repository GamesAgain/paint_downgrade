from core.tools.drawing_tool import DrawingTool
from typing import List, Tuple, Optional
from PyQt6.QtCore import QPointF
from OpenGL.GL import *

class RectangleTool(DrawingTool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.current_point: Optional[QPointF] = None
    
    def get_tool_name(self) -> str:
        return 'rectangle'
    
    def start_drawing(self, point: QPointF, modifiers=None) -> None:
        self.start_point = point
        self.current_point = point
        self.is_drawing = True
    
    def continue_drawing(self, point: QPointF, modifiers=None) -> None:
        if self.is_drawing:
            self.current_point = point
    
    def finish_drawing(self, point: QPointF, modifiers=None) -> List[Tuple[float, float]]:
        if not self.is_drawing or not self.start_point:
            return []
        
        self.current_point = point
        rectangle_points = self._calculate_rectangle_points()
        
        self.is_drawing = False
        self.start_point = None
        self.current_point = None
        
        return rectangle_points
    
    def render(self, color: tuple, width: int) -> None:
        if not self.is_drawing or not self.start_point or not self.current_point:
            return
        
        # Set color and point size for preview
        glColor3f(*color)
        glPointSize(width)
        
        # Draw rectangle preview as points
        glBegin(GL_POINTS)
        rectangle_points = self._calculate_rectangle_points()
        for point in rectangle_points:
            glVertex2f(point[0], point[1])
        glEnd()
    
    def _calculate_rectangle_points(self) -> List[Tuple[float, float]]:
        if not self.start_point or not self.current_point:
            return []
        
        x1, y1 = self.start_point.x(), self.start_point.y()
        x2, y2 = self.current_point.x(), self.current_point.y()
        
        corners = [
            QPointF(x1, y1),
            QPointF(x2, y1),
            QPointF(x2, y2),
            QPointF(x1, y2)
        ]
        
        all_points = []
        for i in range(4):
            start_corner = corners[i]
            end_corner = corners[(i + 1) % 4]
            line_points = self.calculate_bresenham(start_corner, end_corner)
            all_points.extend(line_points)
        
        return all_points