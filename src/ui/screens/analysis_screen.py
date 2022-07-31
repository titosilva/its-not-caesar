from typing import Any, List
from crypto.algorithms.vigenere import VigenereCipher
from crypto.analysis.vigenere_analysis import VigenereAnalyser
from crypto.languages.description import LanguageDescription
from crypto.languages.english import EnglishLanguage
from crypto.languages.portuguese import PortugueseLanguage
from ui.definitions.button import Button
from ui.definitions.container import Container
from ui.definitions.device import Device
from ui.definitions.input import Input
from ui.definitions.interactible import InteractionControl
from ui.definitions.paragraph import Margin, Paragraph
from ui.definitions.renderable import Renderable
from ui.definitions.screen import Screen
from ui.definitions.scroll_menu import ScrollMenu
from ui.definitions.textview import TextView

class AnalysisScreen(Screen):
    def __init__(self, context: Any, ciphertext: str) -> None:
        self.__ciphertext = ciphertext
        self.__analyser = VigenereAnalyser()

        self.key_lengths = []
        self.key_char_scrolls = []
        self.key_length_menu = ScrollMenu(self.key_lengths, on_scroll=self.on_key_length_changed)
        self.detect_language_and_key_lengths()

        device: Device = context.get_device()
        control: InteractionControl = context.get_control()

        self.__device = device
        self.__control = control
        self.__context = context
        screen_size = self.__device.get_size()

        screen_container_config = {
            'border': True, 
            'height': screen_size[0], 
            'width': screen_size[1],
        }
        
        screen_container = Container(configs=screen_container_config)
        key_control = Container(configs={
            'flex': 'row',
        })

        buttons_container = Container(configs={
            'flex': 'row',
            'width': screen_size[1] - 2,
        })
        buttons_container.add_element(
            Button(on_press=self.change_language) 
            % Paragraph("Change language")
        )
        screen_container.add_element(buttons_container)
        screen_container.add_element(Paragraph(self.get_selected_language_text))

        key_control.add_element(Paragraph("Key length: "))
        key_control.add_element(self.key_length_menu)
        key_control.add_element(Margin())
        key_control.add_element(Paragraph("Key value: "))
        self.key_control = key_control
        self.key_char_scrolls = list()
        self.key_chars = Container(configs={
            'flex': 'row',
            'height': 5,
            'width': screen_size[1] - 30,
        }, elements=self.key_char_scrolls)
        self.regenerate_scroll_inputs()
        self.key_control.add_element(self.key_chars)
        screen_container.add_element(self.key_control)

        screen_container.add_element(Paragraph("Deciphered text:"))
        screen_container.add_element(TextView(self.get_deciphered_text, screen_size[1]-2, screen_size[0] - 7))
        self.content: Renderable = screen_container

    def get_selected_language_text(self) -> str:
        return f"Selected language: {self.__selected_language.get_name().lower()}"

    def change_language(self):
        if isinstance(self.__selected_language, PortugueseLanguage):
            self.__selected_language = EnglishLanguage()
        else:
            self.__selected_language = PortugueseLanguage()

        self.key_length_menu.reset()
        self.detect_key_lengths()
        self.draw()

    def detect_language(self):
        self.__selected_language = self.__analyser.detect_language(self.__ciphertext, [EnglishLanguage(), PortugueseLanguage()], max_key_length=20)
    
    def detect_key_lengths(self):
        key_length_characteristics = self.__analyser.compute_avg_characteristic_diff_by_key_length(self.__ciphertext, self.__selected_language, max_key_length=20)
        self.key_lengths.clear()
        self.key_lengths.extend(key_length_characteristics.keys())
        self.key_lengths.sort(key=lambda k: key_length_characteristics[k])
        self.regenerate_scroll_inputs()

    def detect_language_and_key_lengths(self):
        self.detect_language()
        self.detect_key_lengths()

    def regenerate_scroll_inputs(self):
        selected_key_length = self.key_length_menu.current_option
        slices_characteristics_diff_by_key = self.__analyser.get_slices_characteristics_diff_by_key(self.__ciphertext, self.__selected_language, selected_key_length)

        self.key_char_scrolls.clear()
        for i in range(0, selected_key_length):
            slice_char_diff_by_key = slices_characteristics_diff_by_key[i]
            keys = list(slice_char_diff_by_key.keys())
            keys.sort(key=lambda k: abs(slice_char_diff_by_key[k]))

            self.key_char_scrolls.append(Margin())
            self.key_char_scrolls.append(ScrollMenu(keys, on_scroll=self.on_key_char_changed))

    def on_key_length_changed(self):
        self.regenerate_scroll_inputs()
        self.draw()

    def on_key_char_changed(self):
        self.draw()

    def get_deciphered_text(self):
        scrolls = filter(lambda e: isinstance(e, ScrollMenu), self.key_char_scrolls)
        key = ''.join(map(lambda scroll: scroll.current_option, scrolls))
        algorithm = VigenereCipher(alphabet=self.__selected_language.get_alphabet())
        return algorithm(self.__ciphertext, key, 'd')

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
