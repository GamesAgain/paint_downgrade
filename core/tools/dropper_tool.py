from core.tools.drawing_tool import DrawingTool


class DropperTool(DrawingTool):
    def __init__(self, canvas):
        super().__init__(canvas)
        # TODO: Implement dropper tool logic
        pass
    
    def get_tool_name(self) -> str:
        return 'dropper'
    
    def start_drawing(self, point):
        pass
    
    def continue_drawing(self, point):
        pass
    
    def finish_drawing(self, point):
        pass
    
    def render(self, color: tuple, width: int) -> None:
        return super().render(color, width)
