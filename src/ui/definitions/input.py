from typing import Any, Callable, List
from ui.definitions.container import Container
from ui.definitions.interactible import Interactible, InteractionControl
from ui.definitions.paragraph import Paragraph
from ui.definitions.position import Position
from pynput.keyboard import Key

from ui.definitions.utils import Utils


class Input(Interactible):
    def __init__(self, width: int, height: int, position: Position = None, on_changes: Callable = None) -> None:
        super().__init__(position)
        self.__on_changes = on_changes
        self.width = width
        self.height = height
        self.__content = ''

    def render(self) -> List[str]:
        has_border = True if self.height > 2 else False
        text_width = self.width - 2 if has_border else self.width
        text_height = self.height - 2 if has_border else self.height

        text_content = Utils.remove_escape_seqs(self.__content[-(text_width * text_height):])

        subelement = Container(configs={
            'border': True if self.height > 2 else False,
            'width': self.width,
            'height': self.height
        })

        if len(text_content) >= text_width * text_height:
            if self.__interacting:
                text_content = text_content[1:]

            text_content = '…' + text_content[1:]

        row = 0
        while row < text_height:
            limits = (text_width * row, text_width * (row + 1)) 
            line_text = text_content[limits[0]:limits[1]]

            if limits[0] <= len(text_content) and limits[1] > len(text_content):
                if self.__interacting:
                    line_text += Utils.set_green('_')
                else:
                    line_text += '_'

            subelement.add_element(Paragraph(line_text))
            row += 1
        
        return subelement.render()


    def handle_key(self, key: Key, control: InteractionControl):
        key_char = Utils.key_to_char(key)

        if key_char is not None and (str.isalnum(key_char) or str.isspace(key_char)):
            self.__content += key_char
            if self.__on_changes is not None:
                self.__on_changes()
        elif key == Key.backspace:
            self.__content = self.__content[:-1]
            if self.__on_changes is not None:
                self.__on_changes()
        else:
            self.__interacting = False
            control.pass_control(self._parent)

    def take_control(self, control: InteractionControl):
        self.__interacting = True
        return self

