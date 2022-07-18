from typing import List
from ui.definitions.position import Position
from ui.definitions.renderable import Renderable

class Paragraph(Renderable):
    def __init__(self, content: str, position: Position = None) -> None:
        super().__init__(position)
        self.__content = content

    def render(self) -> List[str]:
        return [self.__content]

class Break(Paragraph):
    def __init__(self, position: Position = None) -> None:
        super().__init__('', position)
