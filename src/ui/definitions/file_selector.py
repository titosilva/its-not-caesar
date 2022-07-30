from genericpath import isfile
from pynput.keyboard import Key
from posixpath import abspath
from typing import Any, Callable, List
import os
from ui.definitions.button import Button

from ui.definitions.container import Container
from ui.definitions.interactible import Interactible, InteractionControl
from ui.definitions.paragraph import Paragraph
from ui.definitions.position import Position
from ui.definitions.renderable import Renderable
from ui.definitions.utils import Utils

class FileSelector(Interactible):
    def __init__(self, initial_path: str, width: int, height: int, on_selection_changed: Callable = None, on_selected: Callable[[str], Any] = None, position: Position = None) -> None:
        super().__init__(position)
        self.set_path(initial_path)
        self.width = width
        self.height = height
        self.__interacting = False
        self.__selection = 0

        self.__on_selection_changed = on_selection_changed
        self.__on_selected = on_selected

    def set_path(self, path: str):
        self.__path = path
        dir_path = os.path.abspath(self.__path)

        if os.path.isfile(dir_path):
            (head, tail) = os.path.split(dir_path)

            if head is not None and len(head) > 0:
                dir_path = head
            else:
                dir_path = tail
            
        dir_content = os.listdir(dir_path)
        self.entries = list()
        for file_or_dir in dir_content:
            abs_path = os.path.join(dir_path, file_or_dir)
            self.entries.append((file_or_dir, os.path.isdir(abs_path), abs_path))
        self.entries.sort(key=lambda c: c[1] * '0' + (not c[1]) * '1' + c[0])
        self.entries.insert(0, ('..', True, os.path.split(dir_path)[0]))
        self.__selection = 0

    def render(self) -> List[str]:
        if not os.path.exists(self.__path):
            return Paragraph("Path does not exist").render()

        subcontainer = Container(configs={
            'flex': 'column',
            'width': self.width,
            'height': self.height,
            'border': True
        })

        content_min = self.__selection - self.height // 2
        content_max = self.__selection + self.height // 2

        if content_min < 0:
            content_max += -content_min
            content_min = 0
        elif content_max >= len(self.entries):
            content_min -= content_max - len(self.entries)
            content_max = len(self.entries)

        content_min = max(0, content_min)
        content_max = min(len(self.entries), content_max)

        for idx in range(content_min, content_max):
            entry_info = self.entries[idx]
            entry_content = '⤷ ' if entry_info[1] else '  '
            entry_content += entry_info[0]

            if idx == self.__selection and self.__interacting:
                entry_content = Utils.set_green(entry_content)

            subcontainer.add_element(Paragraph(entry_content))

        return subcontainer.render()

    def handle_key(self, key: Key, control: InteractionControl):
        if key == Key.up:
            self.__selection = (self.__selection - 1) % len(self.entries)
            if self.__on_selection_changed is not None:
                self.__on_selection_changed()
        elif key == Key.down:
            self.__selection = (self.__selection + 1) % len(self.entries)
            if self.__on_selection_changed is not None:
                self.__on_selection_changed()
        elif key == Key.enter:
            entry = self.entries[self.__selection]
            if entry[1]:
                self.set_path(entry[2])
                if self.__on_selection_changed is not None:
                    self.__on_selection_changed()
            else:
                if self.__on_selected is not None:
                    self.__on_selected(entry[2])
                else:
                    self.__interacting = False
                    control.key_to_handle = Key.down
                    control.pass_control(self._parent)
        else:    
            self.__interacting = False
            control.pass_control(self._parent)


    def take_control(self, control: InteractionControl):
        self.__interacting = True
        return self