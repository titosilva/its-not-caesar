from ui.definitions.container import Container
from ui.definitions.screen import ShellScreen
from ui.definitions.paragraph import Paragraph

if __name__ == "__main__":
    screen = ShellScreen()

    screen_size = screen.get_size()
    screen_container_config = {
        'border': True, 
        'height': screen_size[0], 
        'width': screen_size[1], 
        'vertical-align': 'center', 
        'horizontal-align': 'center'
    }
    
    content = \
    Container(configs=screen_container_config) \
        % Paragraph('OK') \
        % Paragraph('Batata')

    screen.draw(content)