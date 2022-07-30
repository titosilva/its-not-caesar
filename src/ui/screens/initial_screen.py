from typing import Any, List
from crypto.languages.english import EnglishLanguage
from ui.definitions.interactible import InteractionControl
from ui.definitions.renderable import Renderable
from ui.definitions.screen import Screen
from ui.definitions.button import Button
from ui.definitions.container import Container
from ui.definitions.device import Device
from ui.definitions.paragraph import Break, Paragraph
from ui.definitions.context import UIContext
from ui.screens.analysis_screen import AnalysisScreen
from ui.screens.cipher_screen import CipherScreen
from ui.screens.ciphertext_file_screen import CiphertextFileScreen

class InitialScreen(Screen):
    def __init__(self, context: UIContext) -> None:
        device: Device = context.get_device()
        control: InteractionControl = context.get_control()

        self.__device = device
        self.__control = control
        self.__context = context

        screen_size = device.get_size()

        screen_container_config = {
            'border': True, 
            'height': screen_size[0], 
            'width': screen_size[1], 
            'vertical-align': 'center', 
            'horizontal-align': 'center'
        }
        
        self.content: Renderable = (
        Container(configs=screen_container_config) 
            % Paragraph("It's not Caesar!") 
            % Paragraph("(Actually, it is Vigenère)") 
            % Paragraph("What would you like to do, my friend?")
            % Break() % (
                Button(on_press=self.go_to_cipher)
                    % Paragraph("Cipher/decipher typed text")
            ) % (
                Button(on_press=self.go_to_analysis)
                    % Paragraph("Crack a ciphertext from file")
            )
        )
            
    def start(self):
        self.__control.set_on_control_passed(self.draw)
        self.__control.pass_control(self.content)
        self.draw()

    def stop(self):
        pass
    
    def go_to_cipher(self):
        self.__context.set_screen(CipherScreen(self.__context))

    def go_to_analysis(self):
        self.__context.set_screen(CiphertextFileScreen(self.__context))

    def draw(self):
        self.__device.draw(self.content.render())