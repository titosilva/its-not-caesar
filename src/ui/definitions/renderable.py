from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List
from pynput.keyboard import Key

from ui.definitions.position import Position

class InteractionControl:
    def __init__(self, context_signaling: Dict[str, Any]) -> None:
        self.__up_control = None
        self.__down_control = None
        self.__left_control = None
        self.__right_control = None
        self.__enter_control = None

        self.__context_signaling = context_signaling

    def set_controls(self, 
        up_control: Callable = None, 
        down_control: Callable = None, 
        left_control: Callable = None, 
        right_control: Callable = None, 
        enter_control: Callable = None):
        self.__up_control = up_control
        self.__down_control = down_control
        self.__left_control = left_control
        self.__right_control = right_control
        self.__enter_control = enter_control

    def handle_key(self, key):
        if key == Key.up and self.__up_control is not None:
            self.__up_control()
        elif key == Key.down and self.__down_control is not None:
            self.__down_control()
        elif key == Key.left and self.__left_control is not None:
            self.__left_control()
        elif key == Key.right and self.__right_control is not None:
            self.__right_control()
        elif key == Key.enter and self.__enter_control is not None:
            self.__enter_control()
        elif key == Key.esc:
            self.__context_signaling['stop'] = True

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

class Interactible(Renderable, ABC):
    @abstractmethod
    def get_control(self, parent, control: InteractionControl):
        raise NotImplementedError()