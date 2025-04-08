import random
from src import Wordle, load_wordlist


def main():
    corpus = load_wordlist("wordlists/wordlist.txt")
    wordle = Wordle(random.choice(corpus))

    while wordle.is_active():
        guess = input("Guess: ")
        pattern = wordle.process_guess(guess)

        print(pattern)
        if wordle.has_won:
            print("You win!")
            break
    else:
        print("Game over...")
        print("The word was: {}".format(wordle.answer))


if __name__ == "__main__":
    main()
