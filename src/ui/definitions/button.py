from typing import Any, Callable, Dict, List
from pynput.keyboard import Key

from ui.definitions.container import Container
from ui.definitions.interactible import InteractionControl
from ui.definitions.position import Position
from ui.definitions.utils import Utils

class Button(Container):
    def __init__(self, position: Position = None, configs: Dict[str, Any] = None, on_press: Callable = None) -> None:
        super().__init__(position, configs)
        self.__on_press = on_press
        self.__interacting = False

    def render(self) -> List[str]:
        result = super().render()

        if len(result) == 0:
            return []

        result = list(map(lambda l: Utils.set_underline(l), result))
        if self.__interacting:   
            result[0] = Utils.set_green(result[0], reset_after=False)
            result[-1] = Utils.reset_after(result[-1])
        
        return result

    def handle_key(self, key: Key, control: InteractionControl):
        if key == Key.enter and self.__on_press is not None:
            self.__on_press()
        else:
            self.__interacting = False
            control.pass_control(self._parent)

    def take_control(self, control: InteractionControl):
        self.__interacting = True
        return self