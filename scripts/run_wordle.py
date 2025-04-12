from src import Wordle


def main(filepath="wordlists/wordlist.csv", generate_answer=False):
    wordle = Wordle(filepath)
    wordle.start_game(
        wordle.wordlist.sample(n=1).values[0] if generate_answer else None
    )


if __name__ == "__main__":
    main()
