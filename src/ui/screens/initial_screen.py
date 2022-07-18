from ui.definitions.container import Container
from ui.definitions.device import Device
from ui.definitions.paragraph import Break, Paragraph

def generate_initial_screen(*args):
    screen: Device = args[0]
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
