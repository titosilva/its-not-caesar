from sys import argv, stdin
from crypto.algorithms.vigenere import VigenereCipher
from ui.definitions.context import UIContext
from ui.screens.initial_screen import InitialScreen

def read_input_lines():
    result = stdin.readlines()

    if len(result) > 0 and len(result[-1]) > 0 and result[-1][-1] == '\n': 
        result[-1] = result[-1][:-1]

    return result

if __name__ == "__main__":
    if len(argv) == 0:
        # If no args, go to interactive mode
        context = UIContext()
        context.set_screen(InitialScreen(context))
        context.launch()

    command = argv[1]

    if len(argv) not in [3, 4] or len(argv[2]) == 0:
        print(argv)
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

    algorithm = VigenereCipher(argv[2])
    if command in ['c', 'cipher']:
        print(algorithm.cipher(text))
    elif command in ['d', 'decipher']:
        print(algorithm.decipher(text))
    else:
        raise Exception(f"Unknown command: {command}")
    