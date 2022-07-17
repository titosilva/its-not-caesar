from abc import ABC, abstractmethod
from typing import List

from ui.definitions.position import Position

class Renderable(ABC):
    def __init__(self, position: Position = None) -> None:
        self.__position = position if position is not None else Position(0, 0)

    def set_position(self, position: Position):
        self.__position = position

    def get_position(self) -> Position:
        return self.__position

    @abstractmethod
    def render(self) -> List[str]:
        raise NotImplementedError()