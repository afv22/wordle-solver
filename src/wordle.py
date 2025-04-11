from collections import Counter
from typing import Optional

from .utils import Color
from .pattern import Pattern


class Wordle:
    def __init__(self, answer: Optional[str] = None):
        self.answer = answer
        self.has_won = False
        self.guesses = []

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

        pattern = Pattern(pattern)
        self.guesses.append({"word": guess, "pattern": pattern})
        self.has_won = pattern.is_winning()
        return pattern

    def is_active(self):
        return len(self.guesses) < 6 and not self.is_won()

    def is_won(self):
        return len(self.guesses) > 0 and self.guesses[-1]['pattern'].is_winning()
