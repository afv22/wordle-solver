from src import Tester

import sys
import random
from collections import Counter

if __name__ == "__main__":
    args = sys.argv[1:]
    iterations = 100 if not len(args) else int(args[0])

    with open("wordlist.txt", "r") as file:
        corpus = file.read().split("\n")

    results = Counter()
    for _ in range(iterations):
        answer = random.choice(corpus)
        num_guesses = Tester.Tester(answer, corpus).run()
        results[num_guesses] += 1

    for i in range(7):
        print("Guesses: {} -> {}".format(i, results[i]))
