from typing import Any, List
from crypto.algorithms.vigenere import VigenereCipher
from ui.definitions.button import Button
from ui.definitions.container import Container
from ui.definitions.device import Device
from ui.definitions.input import Input
from ui.definitions.interactible import InteractionControl
from ui.definitions.paragraph import Margin, Paragraph
from ui.definitions.renderable import Renderable
from ui.definitions.screen import Screen

class CipherScreen(Screen):
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
        self.key_input = Input(screen_size[1] - 13, 1, on_changes=self.on_key_changes)
        self.plaintext_input = Input(screen_size[1] - 2, (screen_size[0] - 4) // 2 - 1, on_changes=self.on_plaintext_changes)
        self.ciphertext_input = Input(screen_size[1] - 2, (screen_size[0] - 4) // 2 - 1, on_changes=self.on_ciphertext_changes)

        key_container = (
            Container(configs={
                'flex': 'row',
                'height': 1,
                'width': screen_size[1] - 2,
            })
            % Paragraph("Key:") 
            % Margin()
            % self.key_input
            % Margin()
            % (
                Button(on_press=self.exit)
                % Paragraph("Exit")
            )
            % Margin()
        )

        plaintext_container = (
            Container(configs={
                'flex': 'column',
                'width': screen_size[1] - 2,
                'height': (screen_size[0] - 4) // 2
            })
            % Paragraph("Plaintext:")
            % self.plaintext_input
        )

        ciphertext_container = (
            Container(configs={
                'flex': 'column',
                'width': screen_size[1] - 2,
                'height': (screen_size[0] - 4) // 2
            })
            % Paragraph("Ciphertext:")
            % self.ciphertext_input
        )

        screen_container.add_element(key_container)
        screen_container.add_element(plaintext_container)
        screen_container.add_element(ciphertext_container)

        self.content: Renderable = screen_container

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

    def on_key_changes(self):
        algorithm = VigenereCipher(self.key_input.get_content())
        plaintext = self.plaintext_input.get_content()
        ciphertext = algorithm(plaintext)
        self.ciphertext_input.set_content(ciphertext)

        self.draw()

    def on_plaintext_changes(self):
        algorithm = VigenereCipher(self.key_input.get_content())
        plaintext = self.plaintext_input.get_content()
        ciphertext = algorithm(plaintext)
        self.ciphertext_input.set_content(ciphertext)
        
        self.draw()

    def on_ciphertext_changes(self):
        algorithm = VigenereCipher(self.key_input.get_content())
        ciphertext = self.ciphertext_input.get_content()
        plaintext = algorithm(ciphertext, mode='d')
        self.plaintext_input.set_content(plaintext)        

        self.draw()