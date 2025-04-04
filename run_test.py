import sys
import random
from collections import Counter

from src import Tester

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 1:
        iterations = int(args[0])
        wordlist_file = args[1]
    else:
        iterations = 10
        wordlist_file = args[0]

    with open(wordlist_file, "r") as file:
        corpus = file.read().split("\n")

    results = Counter()
    for _ in range(iterations):
        answer = random.choice(corpus)
        num_guesses = Tester(answer, corpus).run()
        results[num_guesses] += 1

    for i in range(7):
        print("Guesses: {} -> {}".format(i, results[i]))
