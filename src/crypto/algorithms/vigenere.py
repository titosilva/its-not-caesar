from pydoc import plain
from typing import Callable
from crypto.algorithms.alphabets import Alphabets

class VigenereCipher:
    def __init__(self, key: str = None, alphabet: str = Alphabets.LETTERS) -> None:
        self.__key = key.upper() if key is not None else None
        self.__alphabet = alphabet.upper()
        self.__alphabet_len = len(alphabet)
        
    def __call__(self, text: str, key: str = None, mode: str = 'cipher') -> str:
        if mode.lower() in ['decipher', 'd', 'de', 'dec', 'dc']:
            return self.decipher(text, key)
        elif mode.lower() in ['cipher', 'c', 'ci', 'cip', 'cp']:
            return self.cipher(text, key)

    def cipher(self, plaintext: str, key: str = None) -> str:
        key_to_use = key.upper() if key is not None else self.__key

        if key_to_use is None:
            raise Exception('No key is provided')

        key_len = len(key_to_use)

        if key_len == 0:
            return plaintext

        result = ''
        counter = 0

        # Put all characters to upper to avoid leanking more plaintext message information
        for c in plaintext.upper():
            if c in self.__alphabet:
                src_alpha_idx = self.__alphabet.find(c)
                key_alpha_idx = self.__alphabet.find(key_to_use[counter % key_len])

                if key_alpha_idx < 0:
                    raise Exception(f'Bad key: key character {key_to_use[counter % key_len]} is not in the alphabet')

                dst_alpha_idx = (src_alpha_idx + key_alpha_idx) % self.__alphabet_len

                result += self.__alphabet[dst_alpha_idx]

                counter += 1

        return result

    def decipher(self, ciphertext: str, key: str = None) -> str:
        key_to_use = key.upper() if key is not None else self.__key

        if key_to_use is None:
            raise Exception('No key is provided')
        
        key_len = len(key_to_use)

        if key_len == 0:
            return ciphertext

        result = ''
        counter = 0

        for c in ciphertext:
            c_upper = c.upper()
            if c_upper not in self.__alphabet:
                result += c
            else:
                src_alpha_idx = self.__alphabet.find(c_upper)
                key_alpha_idx = self.__alphabet.find(key_to_use[counter % key_len])
                dst_alpha_idx = (src_alpha_idx - key_alpha_idx) % self.__alphabet_len

                if key_alpha_idx < 0:
                    raise Exception(f'Bad key: key character {key_to_use[counter % key_len]} is not in the alphabet')

                dst_alpha = self.__alphabet[dst_alpha_idx]
                # Keep the provided case to make the text easier to read to the user
                result += dst_alpha.upper() if c.isupper() else dst_alpha.lower()

                counter += 1

        return result
