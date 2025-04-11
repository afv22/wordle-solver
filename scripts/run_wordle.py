from src import Wordle, load_wordlist


def main(filepath="wordlists/wordlist.csv"):
    corpus = load_wordlist(filepath)
    answer = corpus["word"].sample(n=1).iloc[0]
    wordle = Wordle(answer)

    while wordle.is_active():
        guess = input("Guess: ")
        pattern = wordle.process_guess(guess)

        print(pattern)
        if wordle.is_won():
            print("You win!")
            break
    else:
        print("Game over...")
        print("The word was: {}".format(wordle.answer))


if __name__ == "__main__":
    main()
