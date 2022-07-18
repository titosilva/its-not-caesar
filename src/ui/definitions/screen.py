from abc import ABC, abstractmethod
from typing import Tuple
from ui.definitions.renderable import Renderable
import os

class Screen(ABC):
    @abstractmethod
    def draw(self, obj: Renderable):
        raise NotImplementedError()

    @abstractmethod
    def get_size(self) -> Tuple[int, int]:
        raise NotImplementedError()

    @abstractmethod
    def clear(self):
        raise NotImplementedError()

class ShellScreen(Screen):
    def draw(self, obj: Renderable):
        print('\n'.join(obj.render()), end='')

    def get_size(self) -> Tuple[int, int]:
        size = os.get_terminal_size()
        return (size.lines, size.columns)

    def clear(self):
        os.system('clear')