from typing import Callable, List, Union
from ui.definitions.position import Position
from ui.definitions.renderable import Renderable

class Paragraph(Renderable):
    def __init__(self, content: Union[str, Callable], position: Position = None) -> None:
        super().__init__(position)
        self.__content = content

    def render(self) -> List[str]:
        if callable(self.__content):
            return [self.__content()]
        else:
            return [self.__content]

class Break(Paragraph):
    def __init__(self, position: Position = None) -> None:
        super().__init__('', position)

class Margin(Paragraph):
    def __init__(self, size: int = 1, position: Position = None) -> None:
        super().__init__(' ' * size, position)
