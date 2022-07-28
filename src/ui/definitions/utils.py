import re
from typing import Union
from pynput.keyboard import Key, KeyCode

class Utils:
    @staticmethod
    def remove_escape_seqs(text: str) -> str:
        return re.sub(r'\033[\[\;\d]*m', '', text)
    
    @staticmethod
    def replace_keeping_escape_seqs(original_text: str, text_to_insert: str, position: int) -> str:
        final_text = ''
        common_chars_read = 0
        idx = 0

        clean_original_text = Utils.remove_escape_seqs(original_text)
        if position >= len(clean_original_text):
            final_text += original_text
            final_text += ' ' * (position - len(clean_original_text))
            final_text += text_to_insert
            return final_text

        while idx < len(original_text):
            match = re.match(r'\033[\[\;\d]*m', original_text[idx:])

            if match is None:
                common_chars_read += 1

                if common_chars_read > position:
                    final_text += text_to_insert
                    final_text += original_text[idx + len(text_to_insert):]
                    break

                final_text += original_text[idx]
                idx += 1
            else:
                idx += len(match.string)
                final_text += match.string

        return final_text

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
