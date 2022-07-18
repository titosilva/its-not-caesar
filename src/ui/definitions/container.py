from typing import Any, Dict, List, Tuple
from ui.definitions.position import Position
from ui.definitions.renderable import Renderable

class Container(Renderable):
    def __init__(self, position: Position = None, configs: Dict[str, Any] = None) -> None:
        super().__init__(position)

        self.__configs = configs if configs is not None else dict()

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

        if 'width' in configs:
            self.__configs['max-width'] = configs['width']
            self.__configs['min-width'] = configs['width']

        if 'height' in configs:
            self.__configs['max-height'] = configs['height']
            self.__configs['min-height'] = configs['height']

        self.__elements_depth_ordered = list()
    
    def add_element(self, element: Renderable) -> Any:
        self.__elements_depth_ordered.append(element)
        self.__elements_depth_ordered.sort(key=lambda e: e.get_position().depth)
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

            current_render_line = current_render[line_idx - vertical_base]
            horizontal_base = max(0 if horizontal_align != 'center' else (width - len(current_render_line)) // 2, 0)

            padded_render_line = ' ' * horizontal_base + current_render_line
            padded_render_line += ' ' * (width - len(padded_render_line))
            padded_render[line_idx] = padded_render_line

        current_render = padded_render
        return current_render

    def __get_render_sizes(self, current_render: List[str]) -> Tuple[int, int]:
        max_row_len = max(map(lambda line: len(line), current_render))
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
            element_rendered_line = element_rendered[line_idx]
            current_render_line = current_render[line_idx + element_position.row]

            # Right pad the current render with spaces until there is enough
            # space to put the element rendered line
            current_render_line += ' ' * ((len(element_rendered_line) + element_position.col) - len(current_render_line))

            element_line_base = element_position.col
            element_line_end = len(element_rendered_line) + element_line_base
            current_render_line = current_render_line[:element_line_base] + element_rendered_line + current_render_line[element_line_end:]
            current_render[line_idx + element_position.row] = current_render_line

        return current_render

