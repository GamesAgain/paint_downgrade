from typing import Optional, Any

from PyQt6.QtCore import QPointF

from core.tools.drawing_tool import DrawingTool


class MyTool(DrawingTool):
    def start_drawing(self, point: QPointF, modifiers=None) -> None:
        pass

    def continue_drawing(self, point: QPointF, modifiers=None) -> None:
        pass

    def finish_drawing(self, point: QPointF, modifiers=None) -> Optional[Any]:
        pass

    def get_tool_name(self) -> str:
        pass

    def render(self, color: tuple, width: int) -> None:
        pass