from typing import Callable, List, Union
from ui.definitions.container import Container
from ui.definitions.paragraph import Paragraph
from ui.definitions.position import Position
from ui.definitions.renderable import Renderable
from ui.definitions.utils import Utils


class TextView(Renderable):
    def __init__(self, content: Union[str, Callable], width: int, height: int, position: Position = None) -> None:
        super().__init__(position)
        self.__content = content
        self.__width = width
        self.__height = height

    def render(self) -> List[str]:
        content: str
        if callable(self.__content):
            content = self.__content()
        else:
            content = self.__content

        subcontainer = Container(configs={
            'flex': 'column',
            'width': self.__width,
            'height': self.__height,
        })

        max_displayed = self.__width * self.__height
        content = Utils.remove_escape_seqs(content)[:max_displayed]
        chars_displayed = 0
        paragraphs = 0
        while chars_displayed < max_displayed and paragraphs <= self.__height:
            subcontent = content[chars_displayed:chars_displayed+self.__width]

            if '\n' in subcontent:
                line_break_index = subcontent.index('\n')
                subcontent = subcontent[:line_break_index]
                subcontent_padded = subcontent + ' ' * (self.__width - len(subcontent)) 
                subcontainer.add_element(Paragraph(subcontent_padded))
                chars_displayed += len(subcontent) + 2
            else:
                subcontainer.add_element(Paragraph(subcontent))
                chars_displayed += len(subcontent)

            paragraphs += 1

        return subcontainer.render()


