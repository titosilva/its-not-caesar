from abc import ABC, abstractmethod
from typing import Dict, List

class LanguageDescription(ABC): 
    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_alphabet_frequencies(self) -> Dict[str, float]:
        raise NotImplementedError()

    @abstractmethod
    def remove_nonalphabet_chars(self, text: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_alphabet(self) -> List[str]:
        raise NotImplementedError()

    def compute_characteristic(self) -> float:
        freq = self.get_alphabet_frequencies()
        return sum(map(lambda p: p ** 2, freq.values()))

