from typing import Any, List
from crypto.algorithms.vigenere import VigenereCipher
from crypto.languages.description import LanguageDescription
from ui.definitions.button import Button
from ui.definitions.container import Container
from ui.definitions.device import Device
from ui.definitions.input import Input
from ui.definitions.interactible import InteractionControl
from ui.definitions.paragraph import Margin, Paragraph
from ui.definitions.renderable import Renderable
from ui.definitions.screen import Screen
from ui.definitions.scroll_menu import ScrollMenu

class AnalysisScreen(Screen):
    def __init__(self, context: Any, language: LanguageDescription) -> None:
        self.__language = language
        device: Device = context.get_device()
        control: InteractionControl = context.get_control()

        self.__device = device
        self.__control = control
        self.__context = context
        screen_size = self.__device.get_size()

        screen_container_config = {
            'border': True, 
            'height': screen_size[0], 
            'width': screen_size[1],
        }
        
        screen_container = Container(configs=screen_container_config)
        key_control = Container(configs={
            'flex': 'row',
        })

        key_lengths = list(range(5, 20))
        self.key_length_menu = ScrollMenu(key_lengths, on_scroll=self.on_key_lenght_changed)
        key_control.add_element(Paragraph("Key length: "))
        key_control.add_element(self.key_length_menu)
        key_control.add_element(Margin())
        key_control.add_element(Paragraph("Key value: "))

        self.key_control = key_control
        self.key_char_scrolls = list()

        self.key_chars = Container(configs={
            'flex': 'row',
        }, elements=self.key_char_scrolls)

        self.regenerate_scroll_inputs()

        self.key_control.add_element(self.key_chars)
        
        screen_container.add_element(self.key_control)
        self.content: Renderable = screen_container

    def regenerate_scroll_inputs(self):
        self.key_char_scrolls.clear()

        for i in range(0, self.key_length_menu.current_option):
            self.key_char_scrolls.append(Margin())
            self.key_char_scrolls.append(ScrollMenu(self.__language.get_alphabet(), on_scroll=self.on_scroll))

    def on_key_lenght_changed(self):
        self.regenerate_scroll_inputs()
        self.draw()

    def on_scroll(self):
        self.draw()

    def start(self):
        self.__control.set_on_control_passed(self.draw)
        self.__control.pass_control(self.content)
        self.draw()

    def stop(self):
        pass

    def draw(self):
        self.__device.draw(self.content.render())

    def exit(self):
        raise NotImplementedError()
