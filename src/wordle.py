from .companion import Companion
from .pattern import pattern_utils
from .utils import Criteria, load_wordlist


class Wordle:
    def __init__(
        self,
        wordlist_path: str = "wordlists/wordlist.csv",
        criteria: Criteria = Criteria.EXPECTED_MOVES,
    ):
        self.wordlist = load_wordlist(wordlist_path)["word"]
        self.companion = Companion(self.wordlist.to_list(), criteria)

    def start_game(self, answer=None) -> None:
        self.companion.reset()
        guesses = []
        for round in range(1, 7):
            recommended_guess = self.companion.generate_guess(round)
            print(f"Recommended: {recommended_guess}")
            actual_guess = input("Guess: ")

            if answer:
                result_pattern = pattern_utils.calculate_from_guess(
                    actual_guess, answer
                )
            else:
                result_input = input("Result: ")
                result_pattern = pattern_utils.parse_values(result_input)

            self.companion.process_result(actual_guess, result_pattern)
            print(f"{result_pattern} {self.companion.remaining_words()}")

            guesses.append({"word": actual_guess, "pattern": result_pattern})
            if result_pattern.is_correct_guess():
                print("You win!")
                return

        print("Game over!")

    def start_test(self, answer=None, verbose=False) -> int:
        self.companion.reset()

        if not answer:
            answer = self.wordlist.sample(n=1).values[0]

        if verbose:
            print(f"Answer: {answer}")

        guesses = []
        for round in range(1, 7):
            guess = self.companion.generate_guess(round)
            result_pattern = pattern_utils.calculate_from_guess(guess, answer)
            self.companion.process_result(guess, result_pattern)
            if verbose:
                s = "{word}: {pattern} {remaining} words remaining".format(
                    word=guess,
                    pattern=result_pattern,
                    remaining=self.companion.remaining_words(),
                )
                print(s)

            guesses.append({"word": guess, "pattern": result_pattern})
            if result_pattern.is_correct_guess():
                return round

        return -1
