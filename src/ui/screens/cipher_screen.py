from typing import Any, List
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
        
        self.content: Renderable = (
            Container(configs=screen_container_config) 
            % (
                Container(configs={
                    'flex': 'row',
                    'height': screen_size[0] - 2,
                    'width': screen_size[1] - 2,
                })
                % Paragraph("Key:") 
                % Margin()
                % Input(10, 2, on_changes=self.on_key_changes)
                % Margin()
                % (
                    Button(on_press=self.exit)
                    % Paragraph("Exit")
                )
            )
        )

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
        self.draw()