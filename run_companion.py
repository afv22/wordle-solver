import re
import math
from src import WordleSolver, Color


def main(corpus):
    solver = WordleSolver(corpus)
    print("Welcome to your personal Wordle Solver!")
    uncertainty = math.log(len(corpus), 2)

    for i in range(1, 7):
        remaining = solver.remainingWords()
        print("\nRemaining Words: {}".format(remaining))
        if remaining == 0:
            print("Uh oh, I don't know this word!")
            return

        print("Uncertainty: {:.2f}".format(uncertainty))

        guess, expected_entropy = solver.generateGuess()
        print("Guess: {}".format(guess))
        print("Expected Information: {:.2f}".format(expected_entropy))

        result = input("Result: ")
        while not re.search("^([0-2]{5})$", result):
            result = input("Try again: ")

        if result == "11111":
            print("You won in {} guess{}!".format(i, "" if i == 1 else "es"))
            return

        solver.processResult(guess, list(map(Color, map(int, result))))
        
        new_uncertainty = math.log(len(solver.corpus), 2)
        print("Actual Information: {:.2f}".format(uncertainty - new_uncertainty))
        uncertainty = new_uncertainty

    print("Game over. Better luck next time!")


if __name__ == "__main__":
    with open("wordlist.txt", "r") as file:
        corpus = file.read().split("\n")

    main(corpus)
