from abc import ABC, abstractmethod
from typing import List, Tuple
from ui.definitions.renderable import Renderable
import os

class Device(ABC):
    @abstractmethod
    def draw(self, rendered_obj: List[str]):
        raise NotImplementedError()

    @abstractmethod
    def get_size(self) -> Tuple[int, int]:
        raise NotImplementedError()

    @abstractmethod
    def clear(self):
        raise NotImplementedError()

class Shell(Device):
    def draw(self, rendered_obj: List[str]):
        print('\n'.join(rendered_obj), end='')

    def get_size(self) -> Tuple[int, int]:
        size = os.get_terminal_size()
        return (size.lines, size.columns)

    def clear(self):
        os.system('clear')