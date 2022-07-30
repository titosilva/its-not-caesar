from typing import Dict, List
from crypto.languages.description import LanguageDescription
from crypto.utils import strip_accents

class PortugueseLanguage(LanguageDescription):
    def get_name(self) -> str:
        return 'Portuguese'

    def get_alphabet(self) -> List[str]:
        return 'abcdefghijklmnopqrstuvwxyz'

    def remove_nonalphabet_chars(self, text: str) -> str:
        alphabet = self.get_alphabet()
        result = strip_accents(text.lower())
        return ''.join(filter(lambda c: c in alphabet, result))

    # Source: https://www.gta.ufrj.br/grad/06_2/alexandre/criptoanalise.html
    def get_alphabet_frequencies(self) -> Dict[str, float]:
        return {
            'a': 0.1463,
            'b': 0.0104,
            'c': 0.0388,
            'd': 0.0499,
            'e': 0.1257,
            'f': 0.0102,
            'g': 0.0130,
            'h': 0.0128,
            'i': 0.0618,
            'j': 0.0040,
            'k': 0.0002,
            'l': 0.0278,
            'm': 0.0474,
            'n': 0.0505,
            'o': 0.1073,
            'p': 0.0252,
            'q': 0.0120,
            'r': 0.0653,
            's': 0.0781,
            't': 0.0434,
            'u': 0.0463,
            'v': 0.0167,
            'w': 0.0001,
            'x': 0.0021,
            'y': 0.0001,
            'z': 0.0047,
        }