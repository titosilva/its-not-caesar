import re


class Utils:
    @staticmethod
    def remove_escape_seqs(text: str) -> str:
        return re.sub(r'\033[\[\;\d]*m', '', text)