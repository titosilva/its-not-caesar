from abc import ABC, abstractmethod
from typing import Any, Dict
from pynput.keyboard import Key

from ui.definitions.renderable import Renderable


class InteractionControl:
    def __init__(self, context_signaling: Dict[str, Any]) -> None:
        self.__context_signaling = context_signaling
        self.__controller = None

    def pass_control(self, controller: Any, key_to_handle: Key = None):
        self.__controller = controller
        controller.take_control(self)

    def handle_key(self, key: Key):
        if key == Key.esc:
            self.__context_signaling['stop'] = True
            return
        
        if self.__controller is not None:
            self.__controller.handle_key(key, self)

class Interactible(Renderable, ABC):
    @staticmethod
    def is_interactible(element: Any) -> bool:
        return issubclass(type(element), Interactible)

    @abstractmethod
    def handle_key(self, key: Key, control: InteractionControl):
        raise NotImplementedError()

    @abstractmethod
    def take_control(self, control: InteractionControl = None) -> Any:
        raise NotImplementedError()
