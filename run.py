from scripts import run_test, run_wordle, get_input


def main():
    print("Welcome to Wordle!")
    print("Select an experience:")

    options = {
        "1": "Play Wordle",
        "2": "Have a Companion",
        "3": "Run Benchmarker",
    }
    gametype = get_input(options)

    fp = "wordlists/wordlist.csv"
    if gametype == "1":
        run_wordle(filepath=fp, generate_answer=True)
    if gametype == "2":
        run_wordle(filepath=fp)
    elif gametype == "3":
        run_test(filepath=fp)


if __name__ == "__main__":
    main()
