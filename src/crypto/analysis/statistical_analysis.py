from math import sqrt
from typing import Dict, List
from crypto.languages.description import LanguageDescription

class StatisticalAnalyser:
    def __init__(self) -> None:
        pass

    def count_alphabet_on_text(self, text: str, alphabet: List[str]) -> Dict[str, int]:
        result = dict()

        for c in alphabet:
            result[c] = 0

        for c in text:
            if not c in alphabet:
                continue
            
            result[c] += 1

        return result

    def count_alphabet_by_text_slice(self, text: str, alphabet: List[str], number_of_slices: int) -> List[Dict[str, int]]:
        result = list()

        for slice_base in range(0, number_of_slices):
            slice_text = text[slice_base::number_of_slices]
            slice_char_count = self.count_alphabet_on_text(slice_text, alphabet)
            result.append(slice_char_count)

        return result

    def compute_characteristic_from_counts(self, counts: List[int]) -> float:
        total = sum(counts)
        return sum(map(lambda count: (count / total) ** 2, counts))

    def compute_average_value(self, values: List[float]) -> float:
        values_len = len(values)
        return sum(values) / values_len

    def compute_standard_deviation(self, values: List[float]) -> float:
        values_len = len(values)
        values_avg = self.compute_average_value(values)
        return sqrt(sum(map(lambda value: (value - values_avg) ** 2, values)) / values_len)
