import os

from enum import Enum


class Color(Enum):
    GREY = 0
    GREEN = 1
    YELLOW = 2


class Criteria(Enum):
    RANDOM = 0
    ENTROPY = 1
    EXPECTED_MOVES = 2


def load_wordlist(filepath: str) -> list[str]:
    if not os.path.exists(filepath):
        raise ValueError("File does not exist!")

    with open(filepath, "r") as file:
        corpus = file.read()
    return corpus.split("\n")
