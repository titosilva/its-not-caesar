from typing import Any, Callable, List
from ui.definitions.container import Container
from ui.definitions.interactible import Interactible, InteractionControl
from ui.definitions.paragraph import Paragraph
from ui.definitions.position import Position
from pynput.keyboard import Key


class Input(Interactible):
    def __init__(self, width: int, height: int, position: Position = None, on_changes: Callable = None) -> None:
        super().__init__(position)
        self.__on_changes = on_changes
        self.width = width
        self.height = height
        self.__content = ''

    def render(self) -> List[str]:
        subcontent = (
            Container(configs={
                'border': True,
                'width': self.width,
                'height': self.height
            }) % Paragraph(self.__content)
        )
        return subcontent.render()

    def handle_key(self, key: Key, control: InteractionControl):
        if str.isalnum(key.value) or str.isspace(key):
            self.__content += key.value
        elif key == Key.backspace:
            self.__content = self.__content[:-1]
        else:
            self.__interacting = False
            control.pass_control(self._parent)

    def take_control(self, control: InteractionControl):
        self.__interacting = True
        return self

