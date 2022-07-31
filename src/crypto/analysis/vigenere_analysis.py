from typing import Dict, List, Tuple
from crypto.algorithms.vigenere import VigenereCipher
from crypto.analysis.statistical_analysis import StatisticalAnalyser
from crypto.languages.description import LanguageDescription
from crypto.utils import dict_to_ordered_tuples

class VigenereAnalyser:
    def __init__(self) -> None:
        pass

    def detect_language(self, ciphertext: str, possible_languages: List[LanguageDescription], max_key_length: int = None) -> LanguageDescription:
        result = None
        result_avg = None
        for language in possible_languages:
            prepared_text = language.remove_nonalphabet_chars(ciphertext)

            max_possible_key_length = len(prepared_text)
            if max_key_length is not None:
                max_possible_key_length = min(max_possible_key_length, max_key_length)

            min_key_char_diff = None
            for possible_key_length in range(1, max_possible_key_length):
                slices_key_char_diffs = self.get_slices_characteristics_diff_by_key(ciphertext, language, possible_key_length)
                for slice_key_char_diffs in slices_key_char_diffs:
                    min_slice_key_char_diff = min(map(lambda diff: abs(diff), slice_key_char_diffs.values()))
                    if min_key_char_diff is None or min_key_char_diff > min_slice_key_char_diff:
                        min_key_char_diff = min_slice_key_char_diff

            if result_avg is None or min_key_char_diff < result_avg:
                result_avg = min_key_char_diff
                result = language

        return result

    def compute_avg_characteristic_diff_by_key_length(self, ciphertext: str, language: LanguageDescription, max_key_length: int = None) -> Dict[int, float]:
        helper_analyser = StatisticalAnalyser()
        language_characteristic = language.compute_characteristic()
        language_alphabet = language.get_alphabet()
        prepared_text = language.remove_nonalphabet_chars(ciphertext)

        max_possible_key_length = len(prepared_text)
        if max_key_length is not None:
            max_possible_key_length = min(max_possible_key_length, max_key_length)

        avg_characteristics = dict()
        for possible_key_length in range(1, max_possible_key_length):
            slices_counts = helper_analyser.count_alphabet_by_text_slice(prepared_text, language_alphabet, possible_key_length)
            slices_characteristics = list(map(lambda sc: helper_analyser.compute_characteristic_from_counts(sc.values()), slices_counts))
            slices_lang_diffs = list(map(lambda sc: abs(sc - language_characteristic), slices_characteristics))

            avg_characteristics[possible_key_length] = sum(slices_lang_diffs) / len(slices_lang_diffs)

        return avg_characteristics

    def get_most_probable_key(self, ciphertext: str, language: LanguageDescription, key_length: int) -> str:
        helper_analyser = StatisticalAnalyser()
        language_alphabet = language.get_alphabet()
        language_frequencies = language.get_alphabet_frequencies()
        prepared_text = language.remove_nonalphabet_chars(ciphertext)

        language_frequencies_ordered = dict_to_ordered_tuples(language_frequencies)

        key = ''

        for slice_base in range(0, key_length):
            slice_text = prepared_text[slice_base::key_length]
            slice_char_counts = helper_analyser.count_alphabet_on_text(slice_text, language_alphabet)

            slice_char_counts_ordered = dict_to_ordered_tuples(slice_char_counts, reverse=True)

            most_common_alphabet_char_idx = language_alphabet.index(language_frequencies_ordered[0][0])
            most_common_ciphertext_char_idx = language_alphabet.index(slice_char_counts_ordered[0][0])

            print(f'{slice_base}: {most_common_alphabet_char_idx} {most_common_ciphertext_char_idx}')
            slice_key = (most_common_alphabet_char_idx - most_common_ciphertext_char_idx + len(language_alphabet)) % len(language_alphabet)
            key += language_alphabet[slice_key]

        return key

    def get_slices_characteristics_diff_by_key(self, ciphertext: str, language: LanguageDescription, key_length: int = None) -> List[Dict[str, float]]:
        helper_analyser = StatisticalAnalyser()
        language_alphabet = language.get_alphabet()
        language_frequencies = language.get_alphabet_frequencies()
        language_characteristic = language.compute_characteristic()
        prepared_text = language.remove_nonalphabet_chars(ciphertext)

        slices_characteristics_diff_by_key = []

        for slice_base in range(0, key_length):
            slice = prepared_text[slice_base::key_length]
            
            alphabet_counts = helper_analyser.count_alphabet_on_text(slice, language_alphabet)
            total_count = len(slice)
            test_alphabet = list(language_alphabet)
            slice_characteristics_diff_by_key = dict()

            for possible_key_char_idx in range(0, len(language_alphabet)):
                characteristic = sum(language_frequencies[language_alphabet[j]] * alphabet_counts[test_alphabet[j]] / total_count for j in range(0, len(language_alphabet)))
                slice_characteristics_diff_by_key[language_alphabet[possible_key_char_idx]] = characteristic - language_characteristic

                first_element = test_alphabet[0]
                test_alphabet = test_alphabet[1:]
                test_alphabet += first_element

            slices_characteristics_diff_by_key.append(slice_characteristics_diff_by_key)

        return slices_characteristics_diff_by_key

    def get_most_probable_key_v2(self, ciphertext: str, language: LanguageDescription, key_length: int = None):
        helper_analyser = StatisticalAnalyser()
        helper_cipher = VigenereCipher()
        language_alphabet = language.get_alphabet()
        language_frequencies = language.get_alphabet_frequencies()
        language_characteristic = language.compute_characteristic()
        prepared_text = language.remove_nonalphabet_chars(ciphertext)

        guess = ''
        for slice_base in range(0, key_length):
            slice = prepared_text[slice_base::key_length]
            
            alphabet_counts = helper_analyser.count_alphabet_on_text(slice, language_alphabet)
            total_count = len(slice)
            test_alphabet = list(language_alphabet)
            slice_characteristics_by_key = dict()

            for possible_key_char_idx in range(0, len(language_alphabet)):
                characteristic = sum(language_frequencies[language_alphabet[j]] * alphabet_counts[test_alphabet[j]] / total_count for j in range(0, len(language_alphabet)))
                slice_characteristics_by_key[language_alphabet[possible_key_char_idx]] = characteristic - language_characteristic

                last_element = test_alphabet[-1]
                test_alphabet[1:] = test_alphabet[0:-1]
                test_alphabet[0] = last_element

            slice_characteristics_by_key_ordered = dict_to_ordered_tuples(slice_characteristics_by_key)
            if slice_base == 0:
                print('\n'.join(map(lambda t: f'{t[0]}: {t[1]}', slice_characteristics_by_key_ordered)))

            most_probable_slice_key = slice_characteristics_by_key_ordered[0][0]
            guess += most_probable_slice_key

        return guess

        