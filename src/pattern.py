import pickle

from collections import Counter

from .utils import Color
from .cache import Cache


class Pattern(list):
    BLOCKS = {Color.GREEN: "🟩", Color.YELLOW: "🟨", Color.GREY: "⬜"}

    def __init__(self, colors: list[Color]):
        if len(colors) != 5:
            raise ValueError("Invalid number of colors")

        for color in colors:
            self.append(color)

    def is_correct_guess(self):
        return all(map(lambda color: color == Color.GREEN, self))

    def __str__(self):
        return " ".join([self.BLOCKS[color] for color in self])

    def __hash__(self):
        output = 0
        for color in self:
            output *= 10
            output += color.value
        return output


class PatternUtils:
    CACHE_FILE = "pattern_cache.pkl"

    def __init__(self):
        self.cache = Cache(self.CACHE_FILE, 100)
        self.unsaved_pairs = 0

    def parse_values(self, values: list[str | int]) -> Pattern:
        return Pattern(list(map(lambda color: Color(int(color)), values)))

    def calculate_from_guess(self, guess: str, answer: str) -> Pattern:
        """Get the color pattern when 'guess' is played against 'answer'"""
        key = f"{guess}-{answer}"
        if key in self.cache:
            return self.cache[key]

        pattern = [Color.GREY] * len(guess)

        # First pass: mark green matches
        letter_counts = Counter(answer)
        for i, (g, a) in enumerate(zip(guess, answer)):
            if g == a:
                pattern[i] = Color.GREEN
                letter_counts[g] -= 1

        # Second pass: mark yellow matches
        for i, (g, p) in enumerate(zip(guess, pattern)):
            if p == Color.GREY and letter_counts[g] > 0:
                pattern[i] = Color.YELLOW
                letter_counts[g] -= 1

        pattern = Pattern(pattern)
        self.cache[key] = pattern
        return pattern


pattern_utils = PatternUtils()
