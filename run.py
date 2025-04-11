from scripts import run_companion, run_test, run_wordle, get_input


def main():
    print("Welcome to Wordle!")
    print("Select an experience:")

    options = {
        "1": "Play Wordle",
        "2": "Have a Wordle Companion",
        "3": "Run Benchmarker",
    }
    gametype = get_input(options)

    fp = "wordlists/wordlist.csv"
    if gametype == "1":
        run_wordle(filepath=fp)
    elif gametype == "2":
        run_companion(filepath=fp)
    elif gametype == "3":
        run_test(filepath=fp)


main()
