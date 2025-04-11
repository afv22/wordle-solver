import os

import pandas as pd

from enum import Enum


class Color(Enum):
    GREY = 0
    GREEN = 1
    YELLOW = 2


class Criteria(Enum):
    RANDOM = 0
    ENTROPY = 1
    EXPECTED_MOVES = 2


def load_wordlist(filepath: str) -> pd.DataFrame:
    if not os.path.exists(filepath):
        raise ValueError("File does not exist!")
    return pd.read_csv(filepath)
