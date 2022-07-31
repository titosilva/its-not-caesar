from typing import Dict, List, Tuple
from crypto.algorithms.vigenere import VigenereCipher
from crypto.analysis.statistical_analysis import StatisticalAnalyser
from crypto.languages.description import LanguageDescription
from crypto.utils import dict_to_ordered_tuples

class VigenereAnalyser:
    def __init__(self) -> None:
        pass

    def detect_language(self, ciphertext: str, possible_languages: List[LanguageDescription], max_characteristic_diff: float = 0.01, max_slice_characteristic_std_deviation: float = 0.001, max_key_length: int = None) -> LanguageDescription:
        helper_analyser = StatisticalAnalyser()

        result = None
        result_avg = None
        for language in possible_languages:
            language_characteristic = language.compute_characteristic()
            language_alphabet = language.get_alphabet()
            prepared_text = language.remove_nonalphabet_chars(ciphertext)

            max_possible_key_length = len(prepared_text)
            if max_key_length is not None:
                max_possible_key_length = min(max_possible_key_length, max_key_length)

            for possible_key_length in range(1, max_possible_key_length):
                slices_counts = helper_analyser.count_alphabet_by_text_slice(prepared_text, language_alphabet, possible_key_length)
                slices_characteristics = list(map(lambda sc: helper_analyser.compute_characteristic_from_counts(sc.values()), slices_counts))
                slices_lang_diffs = list(map(lambda sc: abs(sc - language_characteristic), slices_characteristics))
                avg = helper_analyser.compute_average_value(slices_lang_diffs)

                if result_avg is None or result_avg > avg:
                    result_avg = avg
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

        lang_digram_characteristic = language.compute_digram_characteristic()
        if lang_digram_characteristic is not None:
            digram_characteristics = self.__get_slices_composed_characteristics_diff_by_key_digrams(
                ciphertext, language, key_length)
            
            for idx in range(0, len(slices_characteristics_diff_by_key)):
                slices_characteristics_diff_by_key[idx] = \
                    helper_analyser.compose_characteristic_diffs(
                        slices_characteristics_diff_by_key[idx],
                        digram_characteristics[idx]
                    )

        return slices_characteristics_diff_by_key

    def __get_slices_composed_characteristics_diff_by_key_digrams(self, ciphertext: str, language: LanguageDescription, key_length: int = None) -> List[Dict[str, float]]:
        helper_analyser = StatisticalAnalyser()
        language_alphabet = language.get_alphabet()
        lang_digram_frequencies = language.get_digram_frequencies()
        lang_digram_characteristic = language.compute_digram_characteristic()
        prepared_text = language.remove_nonalphabet_chars(ciphertext)
        algorithm = VigenereCipher()
        
        # Get all text slices
        slices = list()
        for slice_base in range(0, key_length):
            slices.append(prepared_text[slice_base::key_length])

        avg_slices_characteristics_by_key: List[Dict[str, float]] = list()
        avg_pair_characteristics_by_keys: List[Tuple[Dict[str, float], Dict[str, float]]] = list()

        # Go grouping the text slices on pairs
        for pair_base in range(0, key_length - 1):
            # Join the two consecutive slices
            joined_slices = self.__join_strings_interpolating(slices[pair_base], slices[pair_base + 1])

            # Test different key pairs for the joined slices
            # computing the characteristics for each pair
            key_1_characteristics = dict()
            key_2_characteristics = dict()
            for key_idx_1 in range(0, len(language_alphabet)):
                for key_idx_2 in range(0, len(language_alphabet)):
                    key_1 = language_alphabet[key_idx_1]
                    key_2 = language_alphabet[key_idx_2]
                    key_pair = key_1 + key_2
                    deciphered_joined_slices = algorithm(joined_slices, key_pair, 'd')

                    # Count all digrams on deciphered joined slices
                    digram_count = dict()
                    for digram_base in range(0, len(deciphered_joined_slices), 2):
                        digram = deciphered_joined_slices[digram_base:digram_base + 2]

                        if digram not in digram_count:
                            digram_count[digram] = 0

                        digram_count[digram] += 1
                    
                    # Convert digram count to frequencies then compute the characteristic of the key pair
                    # characteristic = helper_analyser.compute_characteristic_from_counts(digram_count.values())
                    digram_frequency = helper_analyser.counts_to_frequencies(digram_count)
                    characteristic = helper_analyser.compute_characteristic_on_language(digram_frequency, lang_digram_frequencies)

                    # Compute the difference with the language characteristic
                    characteristic_diff = abs(characteristic - lang_digram_characteristic)

                    # Save the characteristicc2[c1_key]
                    if not key_1 in key_1_characteristics:
                        key_1_characteristics[key_1] = []
                    key_1_characteristics[key_1].append(characteristic_diff)

                    if not key_2 in key_2_characteristics:
                        key_2_characteristics[key_2] = []
                    key_2_characteristics[key_2].append(characteristic_diff)

            # Compute the average characteristic diff for key 1 and key 2
            # for this pair base
            key_1_avg_char_diffs = dict()
            for key_1 in key_1_characteristics.keys():
                char_diffs = key_1_characteristics[key_1]
                avg_char_diff = sum(char_diffs)/len(char_diffs)
                key_1_avg_char_diffs[key_1] = avg_char_diff
            
            key_2_avg_char_diffs = dict()
            for key_2 in key_2_characteristics.keys():
                char_diffs = key_2_characteristics[key_2]
                avg_char_diff = sum(char_diffs)/len(char_diffs)
                key_2_avg_char_diffs[key_1] = avg_char_diff

            avg_pair_characteristics_by_keys.append((key_1_avg_char_diffs, key_2_avg_char_diffs))

        # Compose the avg pair characteristics on the final result
        for pair_base in range(0, key_length - 1):
            pair_avg_char_diff = avg_pair_characteristics_by_keys[pair_base]
            slice_characteristics: Dict[str, float]

            if pair_base > 0:
                previous_pair_avg_char_diff = avg_pair_characteristics_by_keys[pair_base - 1]
                slice_characteristics = helper_analyser.compose_characteristic_diffs(
                    pair_avg_char_diff[0], previous_pair_avg_char_diff[1])
            else:
                slice_characteristics = pair_avg_char_diff[0]

            avg_slices_characteristics_by_key.append(slice_characteristics)
        # Add last item
        avg_slices_characteristics_by_key.append(avg_pair_characteristics_by_keys[-1][1])

        return avg_slices_characteristics_by_key


    def __join_strings_interpolating(self, s1: str, s2: str) -> str:
        result = ''
        for idx in range(0, min(len(s1), len(s2))):
            result += f'{s1[idx]}{s2[idx]}'

        if len(s1) > len(s2):
            result += s1[len(s2):]
        elif len(s2) > len(s1):
            result += s2[len(s1):]

        return result


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

        