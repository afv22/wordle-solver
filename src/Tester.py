from collections import Counter

from src import Color, WordleSolver


class Tester:
    def __init__(self, answer, corpus, verbose=False):
        self.answer = answer
        self.solver = WordleSolver(corpus)
        self.verbose = verbose

    def run(self) -> int:
        for i in range(1, 7):
            guess, _ = self.solver.generateGuess()
            pattern = self.generatePattern(guess)
            if self.verbose:
                print("{}: {}".format(guess, pattern))

            if all(map(lambda x: x == Color.GREEN, pattern)):
                return i

            self.solver.processResult(guess, pattern)
        return 0

    def generatePattern(self, guess) -> list[Color]:
        pattern = []
        cntr = Counter(self.answer)
        for i, c in enumerate(guess):
            if cntr[c] == 0:
                pattern.append(Color.GREY)
            elif self.answer[i] == c:
                pattern.append(Color.GREEN)
                cntr[c] -= 1
            else:
                pattern.append(Color.YELLOW)
                cntr[c] -= 1
        return pattern
