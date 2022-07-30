from typing import Any, Dict, List, Tuple
import unicodedata

# Inspiration: https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def dict_to_ordered_tuples(d: Dict[Any, Any], reverse: bool = False) -> List[Tuple[Any, Any]]:
    tuples = list()

    for key in d.keys():
        tuples.append((key, d[key]))

    tuples.sort(key=lambda t: t[1], reverse=reverse)
    return tuples
