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

    def counts_to_frequencies(self, counts: Dict[str, int]) -> Dict[str, float]:
        result = dict()
        total = sum(counts.values())
        for key in counts.keys():
            result[key] = counts[key] / total
        return result

    def compute_characteristic_from_counts(self, counts: List[int]) -> float:
        total = sum(counts)
        return sum(map(lambda count: (count / total) ** 2, counts))

    def compute_characteristic_on_language(self, frequencies: Dict[str, float], language_frequencies: Dict[str, float]):
        result = dict()
        for key in frequencies.keys():
            if key in language_frequencies:
                result[key] = frequencies[key] * language_frequencies[key]

        return sum(result.values()) / len(result.values())

    def compute_average_value(self, values: List[float]) -> float:
        values_len = len(values)
        return sum(values) / values_len

    def compute_standard_deviation(self, values: List[float]) -> float:
        values_len = len(values)
        values_avg = self.compute_average_value(values)
        return sqrt(sum(map(lambda value: (value - values_avg) ** 2, values)) / values_len)

    def compose_characteristic_diffs(self, c1: Dict[str, float], c2: Dict[str, float]) -> Dict[str, float]:
        result = dict()
        
        c2_avg = sum(c2.values())/len(c2.values())
        for c1_key in c1.keys():
            result[c1_key] = c1[c1_key]

            if c1_key in c2:
                c2_value = c2[c1_key]

                if c2_value == 0:
                    continue

                result[c1_key] *= c2_value
            else:
                result[c1_key] *= c2_avg

        return result

