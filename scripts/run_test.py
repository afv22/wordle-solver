import sys

from collections import Counter
from datetime import datetime
from tqdm import tqdm

from src import Wordle
from .utils import get_strategy


def main(filepath="wordlists/wordlist.txt"):
    strategy = get_strategy()
    print("Enter number of iterations:")
    iterations = int(input("> "))

    print("Running benchmarker...")
    start = datetime.now()

    wordle = Wordle(filepath, strategy)
    results = Counter()
    for _ in tqdm(range(iterations), ncols=80):
        result = wordle.start_test()
        results[result] += 1

    end = datetime.now()
    print("Finished in {:.2f}s\n".format((end - start).seconds))

    for i in range(7):
        print("Guesses: {} -> {}".format(i, results[i]))

    print()


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 1:
        iterations = int(args[0])
        filepath = args[1]
    else:
        iterations = 10
        filepath = args[0]

    main(iterations, filepath)
