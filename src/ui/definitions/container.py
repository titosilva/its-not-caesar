from typing import Any, Dict, List, Tuple
from pynput.keyboard import Key

from ui.definitions.interactible import Interactible, InteractionControl
from ui.definitions.position import Position
from ui.definitions.renderable import Renderable
from ui.definitions.utils import Utils

class Container(Interactible):
    def __init__(self, position: Position = None, configs: Dict[str, Any] = None) -> None:
        super().__init__(position)

        self.__configs = configs if configs is not None else dict()

        if 'width' in self.__configs.keys():
            self.__configs['max-width'] = configs['width']
            self.__configs['min-width'] = configs['width']

        if 'height' in self.__configs.keys():
            self.__configs['max-height'] = configs['height']
            self.__configs['min-height'] = configs['height']

        default_configs = {
            'flex': 'column',
            'border': False,
            'max-width': None,
            'max-height': None,
            'min-width': None,
            'min-height': None,
            'vertical-align': 'start',
            'horizontal-align': 'start',
        }

        for config_key in default_configs.keys():
            if config_key not in self.__configs:
                self.__configs[config_key] = default_configs[config_key]

        self.__elements_depth_ordered = list()
        self.__interacting_element = None
    
    def add_element(self, element: Renderable) -> Any:
        self.__elements_depth_ordered.append(element)
        self.__elements_depth_ordered.sort(key=lambda e: e.get_position().depth)
        element.set_parent(self)
        return self

    def __mod__(self, other):
        self.add_element(other)
        return self

    def render(self) -> List[str]:
        current_render = []

        for element in self.__elements_depth_ordered:
            current_render = self.__add_element_to_render(element, current_render)

        current_render = self.__pad_lines(current_render)
        current_render = self.__add_borders(current_render)
        return current_render

    def __pad_lines(self, current_render: List[str]) -> List[str]:
        # Pad all lines to get the same size
        expected_size = self.__get_render_sizes(current_render)
        width = expected_size[0]
        height = expected_size[1]

        min_width = self.__configs['min-width']
        if min_width is not None:
            width = max(width, min_width)
        
        max_width = self.__configs['max-width']
        if max_width is not None:
            if self.__configs['border']:
                max_width -= 2
            width = min(width, max_width)

        min_height = self.__configs['min-height']
        if min_height is not None:
            height = max(height, min_height)

        max_height = self.__configs['max-height']
        if max_height is not None:
            if self.__configs['border']:
                max_height -= 2
            height = min(height, max_height)

        vertical_align = self.__configs['vertical-align']
        horizontal_align = self.__configs['horizontal-align']

        vertical_base = max(0 if vertical_align != 'center' else (height - len(current_render)) // 2, 0)

        padded_render = list()
        for line_idx in range(0, height):
            if line_idx < vertical_base or line_idx - vertical_base >= len(current_render):
                padded_render.append(' ' * width)
                continue

            if line_idx >= len(padded_render):
                padded_render.append('')

            current_render_line_raw = current_render[line_idx - vertical_base]
            current_render_line = Utils.remove_escape_seqs(current_render_line_raw)
            horizontal_base = max(0 if horizontal_align != 'center' else (width - len(current_render_line)) // 2, 0)

            padded_render_line = ' ' * horizontal_base + current_render_line_raw
            padded_render_line += ' ' * (width - (horizontal_base + len(current_render_line)))
            padded_render[line_idx] = padded_render_line

        current_render = padded_render
        return current_render

    def __get_render_sizes(self, current_render: List[str]) -> Tuple[int, int]:
        if len(current_render) == 0:
            return (0, 0)

        max_row_len = max(map(lambda line: len(Utils.remove_escape_seqs(line)), current_render))
        return (max_row_len, len(current_render))

    def __add_borders(self, current_render: List[str]) -> List[str]:
        if self.__configs['border']:
            current_size = self.__get_render_sizes(current_render)
            up_down_borders = '―' * current_size[0]
            current_render.insert(0, up_down_borders)
            current_render.append(up_down_borders)

            for line_idx in range(0, len(current_render)):
                render_line = current_render[line_idx]

                if line_idx == 0:
                    render_line = '┌' + render_line + '┐'
                elif line_idx == len(current_render) - 1:
                    render_line = '└' + render_line + '┘'
                else:
                    render_line = '│' + render_line + '│'

                current_render[line_idx] = render_line

        return current_render

    def __add_element_to_render(self, element: Renderable, current_render: List[str]) -> List[str]:
        if self.__configs['flex'] == 'column':
            element.set_position(Position(len(current_render), element.get_position().col))

        element_rendered = element.render()
        element_position = element.get_position()

        # Bottom pad the current render with empty lines until 
        # there are enough lines to put the element lines
        current_render += [''] * ((len(element_rendered) + element_position.row) - len(current_render))

        for line_idx in range(0, len(element_rendered)):
            element_rendered_line_raw = element_rendered[line_idx]
            element_rendered_line = Utils.remove_escape_seqs(element_rendered_line_raw)
            current_render_line = current_render[line_idx + element_position.row]

            # Right pad the current render with spaces until there is enough
            # space to put the element rendered line
            current_render_line += ' ' * ((len(element_rendered_line) + element_position.col) - len(current_render_line))

            element_line_base = element_position.col
            element_line_end = len(element_rendered_line) + element_line_base
            current_render_line = current_render_line[:element_line_base] + element_rendered_line_raw + current_render_line[element_line_end:]
            current_render[line_idx + element_position.row] = current_render_line

        return current_render

    def __get_next_element(self, direction: str):
        interactibles = list(filter(lambda e: Interactible.is_interactible(e), self.__elements_depth_ordered))

        if len(interactibles) == 0:
            return None

        if len(interactibles) == 1 and self.__interacting_element is not None:
            return None
        
        if self.__interacting_element is None:
            return interactibles[0]
        
        filtered: List[Interactible] = []
        current_row = self.__interacting_element.get_position().row
        current_col = self.__interacting_element.get_position().col

        if direction in ['up', 'down']:
            if direction == 'up':
                filtered = list(filter(lambda e: e.get_position().row < current_row, interactibles))
            else:
                filtered = list(filter(lambda e: e.get_position().row > current_row, interactibles))

            if len(filtered) == 0:
                return None

            filtered.sort(key=lambda e: abs(current_row - e.get_position().row))
            return filtered[0]
        elif direction in ['left', 'right']:
            if direction == 'left':
                filtered = list(filter(lambda e: e.get_position().col < current_col, interactibles))
            else:
                filtered = list(filter(lambda e: e.get_position().col > current_col, interactibles))

            if len(filtered) == 0:
                return None

            filtered.sort(key=lambda e: abs(current_col - e.get_position().col))
            return filtered[0]

        return None

    def handle_key(self, key: Key, control: InteractionControl):
        next_element: Interactible = None

        if key == Key.up:
            next_element = self.__get_next_element('up')
        elif key == Key.down:
            next_element = self.__get_next_element('down')
        elif key == Key.left:
            next_element = self.__get_next_element('left')
        elif key == Key.right:
            next_element = self.__get_next_element('right')
        else:
            return
        
        if next_element is None:
            if self._parent is not None:
                control.pass_control(self._parent, key_to_handle=key)
                self.__interacting_element = None
            elif self.__interacting_element is not None:
                control.pass_control(self.__interacting_element)
                
            return

        self.__interacting_element = next_element
        control.pass_control(next_element)

    def take_control(self, control: InteractionControl):
        interactibles = list(filter(lambda e: Interactible.is_interactible(e), self.__elements_depth_ordered))

        if len(interactibles) == 0:
            return

        if self.__interacting_element is None:
            self.__interacting_element = interactibles[0]
            control.pass_control(self.__interacting_element)
            return

        if control.key_to_handle is not None:
            self.handle_key(control.key_to_handle, control)
        