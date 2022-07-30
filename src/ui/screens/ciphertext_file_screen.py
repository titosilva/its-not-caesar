from typing import Any, List
from crypto.algorithms.vigenere import VigenereCipher
from ui.definitions.button import Button
from ui.definitions.container import Container
from ui.definitions.device import Device
from ui.definitions.file_selector import FileSelector
from ui.definitions.input import Input
from ui.definitions.interactible import InteractionControl
from ui.definitions.paragraph import Margin, Paragraph
from ui.definitions.renderable import Renderable
from ui.definitions.screen import Screen
from ui.screens.analysis_screen import AnalysisScreen

class CiphertextFileScreen(Screen):
    def __init__(self, context: Any) -> None:
        device: Device = context.get_device()
        control: InteractionControl = context.get_control()

        self.__device = device
        self.__control = control
        self.__context = context

        self.__device = device
        screen_size = device.get_size()

        screen_container_config = {
            'border': True, 
            'height': screen_size[0], 
            'width': screen_size[1],
            'vertical-align': 'center', 
            'horizontal-align': 'center'
        }

        screen_container = Container(configs=screen_container_config)
        screen_container.add_element(Paragraph("Navigate and select the ciphertext file:"))
        screen_container.add_element(
            FileSelector('.', screen_size[1] - 2, screen_size[0] - 3, 
                on_selection_changed=self.draw, 
                on_selected=self.open_file
            )
        )
        self.content = screen_container


    def start(self):
        self.__control.set_on_control_passed(self.draw)
        self.__control.pass_control(self.content)
        self.draw()

    def stop(self):
        pass

    def draw(self):
        self.__device.draw(self.content.render())

    def open_file(self, path: str):
        with open(path, 'r') as f:
            ciphertext = '\n'.join(f.readlines())
            self.__context.set_screen(AnalysisScreen(self.__context, ciphertext=ciphertext))

