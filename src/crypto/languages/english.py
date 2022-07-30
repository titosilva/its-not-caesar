from typing import Dict, List
from crypto.languages.description import LanguageDescription
from crypto.utils import strip_accents

class EnglishLanguage(LanguageDescription):
    def get_name(self) -> str:
        return 'English'

    def get_alphabet(self) -> List[str]:
        return 'abcdefghijklmnopqrstuvwxyz'

    def remove_nonalphabet_chars(self, text: str) -> str:
        alphabet = self.get_alphabet()
        result = strip_accents(text.lower())
        return ''.join(filter(lambda c: c in alphabet, result))

    # Source: https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
    def get_alphabet_frequencies(self) -> Dict[str, float]:
        return {
            'a': 0.084966,
            'b': 0.020720,
            'c': 0.045388,
            'd': 0.033844,
            'e': 0.111607,
            'f': 0.018121,
            'g': 0.024705,
            'h': 0.030034,
            'i': 0.075448,
            'j': 0.001965,
            'k': 0.011016,
            'l': 0.054893,
            'm': 0.030129,
            'n': 0.066544,
            'o': 0.071635,
            'p': 0.031671,
            'q': 0.001962,
            'r': 0.075809,
            's': 0.057351,
            't': 0.069509,
            'u': 0.033844,
            'v': 0.010074,
            'w': 0.012899,
            'x': 0.002902,
            'y': 0.017779,
            'z': 0.002722,
        }
        