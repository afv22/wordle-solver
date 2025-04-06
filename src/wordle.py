from collections import Counter
from typing import Optional

from .colors import Color
from .pattern import Pattern


class Wordle:
    def __init__(self, answer: Optional[str] = None):
        self.answer = answer
        self.has_won = False
        self.guess_number = 1

    def process_guess(self, guess: str) -> Pattern:
        if not self.is_active():
            raise ValueError("Game is complete!")

        colors = []
        cntr = Counter(self.answer)
        for i, c in enumerate(guess):
            if cntr[c] == 0:
                colors.append(Color.GREY)
            elif self.answer[i] == c:
                colors.append(Color.GREEN)
                cntr[c] -= 1
            else:
                colors.append(Color.YELLOW)
                cntr[c] -= 1

        self.guess_number += 1
        pattern = Pattern(colors)
        self.has_won = pattern.is_winning()
        return pattern

    def is_active(self):
        return self.guess_number <= 6 and not self.has_won
