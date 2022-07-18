from ui.definitions.container import Container
from ui.definitions.context import UIContext
from ui.definitions.renderable import InteractionControl
from ui.definitions.screen import Screen, ShellScreen
from ui.definitions.paragraph import Break, Paragraph

def generate_main_screen(*args):
    screen: Screen = args[0]
    screen_size = screen.get_size()

    # last_screen_size = screen_size
    screen_container_config = {
        'border': True, 
        'height': screen_size[0], 
        'width': screen_size[1], 
        'vertical-align': 'center', 
        'horizontal-align': 'center'
    }
    
    content = \
    Container(configs=screen_container_config) \
        % Paragraph("It's not Caesar!") \
        % Paragraph("(Actually, it is Vigenère)") \
        % Break() \
        % Paragraph("Click here to cipher")

    return content

if __name__ == "__main__":
    context = UIContext()
    context.set_ui_content(generate_main_screen)
    context.launch()