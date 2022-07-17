from ui.definitions.container import Container
from ui.definitions.screen import ShellScreen
from ui.definitions.paragraph import Paragraph

if __name__ == "__main__":
    screen = ShellScreen()

    screen_size = screen.get_size()
    
    content = \
    Container(configs={'border': True, 'height': screen_size[0], 'width': screen_size[1]}) \
        % Paragraph('OK') \
        % Paragraph('Batata')

    screen.draw(content)