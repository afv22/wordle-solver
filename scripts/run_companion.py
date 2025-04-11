import re
import sys

from src import Pattern, WordleSolver, load_wordlist
from .utils import get_strategy


def main(filepath="wordlists/dracos_wordlist.csv"):
    print("Welcome to your personal Wordle Solver!")

    solver = WordleSolver(load_wordlist(filepath)["word"].to_list(), get_strategy())
    uncertainty = solver.get_uncertainty()

    for i in range(6):
        print("\nRemaining Words: {}".format(solver.remainingWords()))
        print("Uncertainty: {:.2f}".format(uncertainty))

        recommended_guess, expected_information = solver.generate_guess(i)
        print("Recommended Guess: {}".format(recommended_guess))
        print("Expected Information: {:.2f} bits".format(expected_information))
        guess = input('Actual Guess: ')
        result = input("Result: ")
        while not re.search("^([0-2]{5})$", result):
            result = input("Try again: ")

        if result == "11111":
            print("You won in {} guess{}!".format(i + 1, "" if i == 0 else "es"))
            return

        solver.process_result(guess, Pattern(result))

        if solver.remainingWords() == 0:
            print("Uh oh, I don't know this word!")
            return

        new_uncertainty = solver.get_uncertainty()
        print("Actual Information: {:.2f} bits".format(uncertainty - new_uncertainty))
        uncertainty = new_uncertainty

    print("Game over. Better luck next time!")


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 1:
        filepath = args[0]
    else:
        filepath = "wordlists/dracos_wordlist.txt"

    main(filepath)
