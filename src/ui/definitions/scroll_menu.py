from typing import Any, Callable, List, Union
from ui.definitions.container import Container
from ui.definitions.interactible import Interactible, InteractionControl
from ui.definitions.paragraph import Paragraph
from ui.definitions.position import Position
from pynput.keyboard import Key

from ui.definitions.utils import Utils

class ScrollMenu(Interactible):
    def __init__(self, options: List[Union[str, int]], position: Position = None, on_scroll: Callable = None) -> None:
        super().__init__(position)
        self.__on_scroll = on_scroll
        self.options = options
        self.current_position = 0
        self.__interacting = False

    def set_parent(self, parent):
        return super().set_parent(parent)

    @property
    def current_option(self):
        return self.options[self.current_position]

    def render(self) -> List[str]:
        option_content_raw = str(self.options[self.current_position])
        option_content = Utils.remove_escape_seqs(option_content_raw)

        subelement = Container(configs={
            'flex': 'column',
            'width': len(option_content),
            'height': 5,
            'border': False,
        })

        whitespaces = ' ' * len(option_content)
        position = self.current_position

        subelement.add_element(Paragraph(str(self.options[self.current_position - 1])[:len(option_content)] if position > 0 else whitespaces))
        subelement.add_element(Paragraph('▲' * len(option_content) if position > 0 else whitespaces))

        if self.__interacting:
            subelement.add_element(Paragraph(Utils.set_inverted(Utils.set_green(option_content_raw))))
        else:
            subelement.add_element(Paragraph(option_content_raw))

        subelement.add_element(Paragraph('▼' * len(option_content) if position < len(self.options) - 1 else whitespaces))
        subelement.add_element(Paragraph(str(self.options[self.current_position + 1])[:len(option_content)] if position < len(self.options) - 1 else whitespaces))

        return subelement.render()


    def handle_key(self, key: Key, control: InteractionControl):
        if key == Key.up:
            if self.current_position > 0:
                self.current_position -= 1

            if self.__on_scroll is not None:
                self.__on_scroll()
            return
        elif key == Key.down:
            if self.current_position < len(self.options) - 1:
                self.current_position += 1

            if self.__on_scroll is not None:
                self.__on_scroll()
            return
        else:
            self.__interacting = False
            control.pass_control(self._parent)

    def take_control(self, control: InteractionControl):
        self.__interacting = True
        return self

