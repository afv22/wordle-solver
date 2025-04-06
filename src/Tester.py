from collections import Counter

from src import Cache, Criteria, WordleSolver, Wordle


class Tester:
    def __init__(
        self,
        answer: str,
        corpus: list[str],
        criteria: Criteria,
        verbose: bool = False,
        entropy_cache: Cache = None,
        pattern_cache: Cache = None,
    ):
        self.wordle = Wordle(answer)
        self.solver = WordleSolver(corpus, criteria, entropy_cache, pattern_cache)
        self.verbose = verbose

    def run(self) -> int:
        while self.wordle.is_active():
            guess, _ = self.solver.generate_guess(self.wordle.guess_number)
            pattern = self.wordle.process_guess(guess)
            self.solver.process_result(guess, pattern)
            if self.verbose:
                print("{}: {}".format(guess, pattern))

        return self.wordle.guess_number if self.wordle.has_won else 0
