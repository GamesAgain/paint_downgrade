from core.tools.drawing_tool import DrawingTool
from typing import List, Tuple, Optional
from PyQt6.QtCore import QPointF
from OpenGL.GL import *
from PyQt6.QtCore import Qt
import math


class CircleTool(DrawingTool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.current_point: Optional[QPointF] = None
        self.modifiers = None
    
    def get_tool_name(self) -> str:
        return 'circle'
    
    def start_drawing(self, point: QPointF, modifiers=None) -> None:
        self.start_point = point
        self.current_point = point
        self.modifiers = modifiers
        self.is_drawing = True
    
    def continue_drawing(self, point: QPointF, modifiers=None) -> None:
        if self.is_drawing:
            self.current_point = point
            self.modifiers = modifiers
    
    def finish_drawing(self, point: QPointF, modifiers=None) -> List[Tuple[float, float]]:
        if not self.is_drawing or not self.start_point:
            return []
        
        self.current_point = point
        self.modifiers = modifiers
        shape_points = self._calculate_shape_points()
        
        self.is_drawing = False
        self.start_point = None
        self.current_point = None
        self.modifiers = None
        
        return shape_points
    
    def render(self, color: tuple, width: int) -> None:
        if not self.is_drawing or not self.start_point or not self.current_point:
            return
        
        # Set color and point size for preview
        glColor3f(*color)
        glPointSize(width)
        
        # Draw shape preview as points
        glBegin(GL_POINTS)
        shape_points = self._calculate_shape_points()
        for point in shape_points:
            glVertex2f(point[0], point[1])
        glEnd()
    
    def _calculate_shape_points(self) -> List[Tuple[float, float]]:
        if not self.start_point or not self.current_point:
            return []
        
        # Calculate center and dimensions
        cx = self.start_point.x()
        cy = self.start_point.y()
        dx = abs(self.current_point.x() - cx)
        dy = abs(self.current_point.y() - cy)
        
        # Check if Shift is pressed for perfect circle
        if self.modifiers and Qt.KeyboardModifier.ShiftModifier in self.modifiers:
            # Perfect circle - use the smaller dimension as radius
            radius = int(min(dx, dy))
            return self._calculate_circle_points(cx, cy, radius)
        else:
            # Ellipse
            return self._calculate_ellipse_points(cx, cy, dx, dy)
    
    def _calculate_circle_points(self, cx: float, cy: float, radius: int) -> List[Tuple[float, float]]:
        if radius == 0:
            return []
        
        # Use midpoint circle algorithm
        points = []
        x = 0
        y = radius
        d = 1 - radius
        
        while x <= y:
            # Add all 8 octant points
            points.extend([
                (cx + x, cy + y), (cx - x, cy + y),
                (cx + x, cy - y), (cx - x, cy - y),
                (cx + y, cy + x), (cx - y, cy + x),
                (cx + y, cy - x), (cx - y, cy - x)
            ])
            
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1
        
        return points
    
    def _calculate_ellipse_points(self, cx: float, cy: float, rx: float, ry: float) -> List[Tuple[float, float]]:
        if rx == 0 or ry == 0:
            return []
        
        points = []
        # Use parametric equation for ellipse
        num_points = max(int(rx), int(ry)) * 4  # More points for smoother ellipse
        
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            x = cx + rx * math.cos(angle)
            y = cy + ry * math.sin(angle)
            points.append((x, y))
        
        return points

