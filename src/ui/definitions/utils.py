import re
from typing import Union
from pynput.keyboard import Key, KeyCode

class Utils:
    @staticmethod
    def remove_escape_seqs(text: str) -> str:
        return re.sub(r'\033[\[\;\d]*m', '', text)

    @staticmethod
    def set_green(text: str, set_white_after: bool = True) -> str:
        if set_white_after:
            return Utils.set_white_after('\033[38;5;10m' + text)

        return '\033[38;5;10m' + text

    @staticmethod
    def set_white_after(text: str) -> str:
        return text + '\033[38;5;15m'

    @staticmethod
    def key_to_char(key: Union[Key, KeyCode]):
        if isinstance(key, Key):
            return key.value.char
        
        return key.char
