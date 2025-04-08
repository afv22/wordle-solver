from collections import Counter
from typing import Optional

from .utils import Color
from .pattern import Pattern


class Wordle:
    def __init__(self, answer: Optional[str] = None):
        self.answer = answer
        self.has_won = False
        self.guesses_made = 0

    def process_guess(self, guess: str) -> Pattern:
        if not self.is_active():
            raise ValueError("Game is complete.")

        pattern = [Color.GREY] * len(guess)

        # First pass: mark green matches
        letter_counts = Counter(self.answer)
        for i, (g, a) in enumerate(zip(guess, self.answer)):
            if g == a:
                pattern[i] = Color.GREEN
                letter_counts[g] -= 1

        # Second pass: mark yellow matches
        for i, (g, p) in enumerate(zip(guess, pattern)):
            if p == Color.GREY and letter_counts[g] > 0:
                pattern[i] = Color.YELLOW
                letter_counts[g] -= 1


        self.guesses_made += 1
        pattern = Pattern(pattern)
        self.has_won = pattern.is_winning()
        return pattern

    def is_active(self):
        return self.guesses_made < 6 and not self.has_won
