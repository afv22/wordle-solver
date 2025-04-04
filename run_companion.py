from src.WordleSolver import WordleSolver
import re
from collections import Counter
from src.colors import Color


def main(corpus):
    solver = WordleSolver(corpus)
    print("Welcome to your personal Wordle Solver!")

    for i in range(1, 7):
        remaining = solver.remainingWords()
        print("\nRemaining Words: {}".format(remaining))
        if remaining == 0:
            print("Uh oh, I don't know this word!")
            return

        guess = solver.generateGuess()
        print("Guess: {}".format(guess))

        result = input("Result: ")
        while not re.search("^([0-2]{5})$", result):
            result = input("Try again: ")

        if result == "11111":
            print("You won in {} guess{}!".format(i, "" if i == 1 else "es"))
            return

        solver.processResult(guess, list(map(Color, map(int, result))))

    print("Game over. Better luck next time!")


if __name__ == "__main__":
    with open("wordlist.txt", "r") as file:
        corpus = file.read().split("\n")
    
    main(corpus)
