from scripts.run_wordle import main as run_wordle
from scripts.run_companion import main as run_companion
from scripts.run_test import main as run_test


def main():
    print("Welcome to Wordle!")
    print("Would you like to:")

    options = {
        "1": "Play Wordle",
        "2": "Have a Wordle Companion",
        "3": "Run Benchmarker",
    }

    for key in options:
        print(f"{key}: {options[key]}")

    gametype = input("> ")
    while gametype not in options.keys():
        print("Oops! Try again.")
        gametype = input("> ")

    if gametype == "1":
        run_wordle()
    elif gametype == "2":
        run_companion()
    elif gametype == "3":
        run_test()


main()
