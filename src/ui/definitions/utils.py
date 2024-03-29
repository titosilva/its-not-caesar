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
            match = re.match(r'^\033[\[\;\d]+m', original_text[idx:])

            if match is None:
                common_chars_read += 1

                if common_chars_read > position:
                    final_text += text_to_insert
                    final_text += original_text[idx + len(text_to_insert):]
                    break

                final_text += original_text[idx]
                idx += 1
            else:
                matched_text = match.group()
                idx += len(matched_text)
                final_text += matched_text

        return final_text

    @staticmethod
    def set_green(text: str, reset_after: bool = True) -> str:
        if reset_after:
            return Utils.reset_after('\033[38;5;10m' + text)

        return '\033[38;5;10m' + text

    @staticmethod
    def set_underline(text: str, reset_after: bool = True) -> str:
        result = '\033[4m' + text

        if reset_after:
            return Utils.reset_after(result)

        return result

    @staticmethod
    def set_inverted(text: str, reset_after: bool = True) -> str:
        result = '\033[33;7m' + text

        if reset_after:
            return Utils.reset_after(result)

        return result

    @staticmethod
    def reset_after(text: str) -> str:
        return text + '\033[0m'

    @staticmethod
    def key_to_char(key: Union[Key, KeyCode]):
        if isinstance(key, Key):
            return key.value.char
        
        return key.char
