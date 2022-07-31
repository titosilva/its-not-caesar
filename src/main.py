from sys import argv, stdin
from typing import Tuple
from crypto.algorithms.vigenere import VigenereCipher
from ui.definitions.context import UIContext
from ui.screens.analysis_screen import AnalysisScreen
from ui.screens.initial_screen import InitialScreen

def read_input_lines():
    result = stdin.readlines()

    if len(result) > 0 and len(result[-1]) > 0 and result[-1][-1] == '\n': 
        result[-1] = result[-1][:-1]

    return result

def check_cipher_args_and_get_text_and_key() -> Tuple[str, str]:
    if len(argv) not in [3, 4] or len(argv[2]) == 0:
        raise Exception("Missing key")

    text: str

    if len(argv) == 4 and len(argv[3]) > 0:
        text = argv[3]
    else:
        input_lines = read_input_lines()
        if len(input_lines) != 0:
            text = '\n'.join(input_lines)
        else:
            raise Exception("Missing text")

    key = argv[2]
    return (text, key)

def check_analysis_args_and_get_text() -> str:
    if len(argv) < 2:
        raise Exception("Missing file name")

    text: str
    file_path = argv[2]
    with open(file_path, 'r') as f:
        text = f.read()

    return text

if __name__ == "__main__":
    if len(argv) < 2:
        # If no args, go to interactive mode
        context = UIContext()
        context.set_screen(InitialScreen(context))
        context.launch()
    else:
        command = argv[1]

        if command in ['analyse', 'analysis', 'crack']:
            text = check_analysis_args_and_get_text()
            context = UIContext()
            context.set_screen(AnalysisScreen(context, text))
            context.launch()
        elif command in ['c', 'cipher']:
            text, key = check_cipher_args_and_get_text_and_key()
            algorithm = VigenereCipher(key)
            print(algorithm.cipher(text))
        elif command in ['d', 'decipher']:
            text, key = check_cipher_args_and_get_text_and_key()
            algorithm = VigenereCipher(key)
            print(algorithm.decipher(text))
        else:
            raise Exception(f"Unknown command: {command}")
        