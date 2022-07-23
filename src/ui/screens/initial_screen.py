from typing import Any, List
from ui.definitions.interactible import InteractionControl
from ui.definitions.renderable import Renderable
from ui.definitions.screen import Screen
from ui.definitions.button import Button
from ui.definitions.container import Container
from ui.definitions.device import Device
from ui.definitions.paragraph import Break, Paragraph

class InitialScreen(Screen):
    def __init__(self, context: Any) -> None:
        device: Device = context.get_device()
        control: InteractionControl = context.get_control()

        self.__button_content = 'ON'
        self.__device = device

        screen_size = device.get_size()

        # last_screen_size = screen_size
        screen_container_config = {
            'border': True, 
            'height': screen_size[0], 
            'width': screen_size[1], 
            'vertical-align': 'center', 
            'horizontal-align': 'center'
        }
        
        self.content: Renderable = \
        Container(configs=screen_container_config) \
            % Paragraph("It's not Caesar!") \
            % Paragraph("(Actually, it is Vigenère)") \
            % Break() \
            % Button(on_press=self.toggle_button_content).add_element(Paragraph(self.get_button_content))

        control.pass_control(self.content)
        self.__device.clear()
        self.__device.draw(self.content.render())

    def get_content(self) -> Renderable:
        return self.content

    def get_rendered_content(self) -> List[str]:
        return self.content.render()

    def toggle_button_content(self):
        self.__button_content = 'OFF' if self.__button_content == 'ON' else 'ON'
        self.__device.clear()
        self.__device.draw(self.content.render())

    def set_context(self, context: Any) -> Renderable:
        self.__context = context

    def get_button_content(self):
        return self.__button_content