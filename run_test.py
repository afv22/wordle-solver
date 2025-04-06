import random
import sys
from collections import Counter
from datetime import datetime
from tqdm import tqdm

from src import Cache, Criteria, Tester

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 1:
        iterations = int(args[0])
        wordlist_file = args[1]
    else:
        iterations = 10
        wordlist_file = args[0]

    print("Loading wordlist...")
    with open(wordlist_file, "r") as file:
        corpus = file.read().split("\n")

    print("Running benchmarker...")
    start = datetime.now()

    results = Counter()
    entropy_cache = Cache("entropy_cache.pkl")
    pattern_cache = Cache("pattern_cache.pkl")
    for _ in tqdm(range(iterations), ncols=80):
        answer = random.choice(corpus)
        num_guesses = Tester(
            answer,
            corpus,
            Criteria.RANDOM,
            entropy_cache=entropy_cache,
            pattern_cache=pattern_cache,
        ).run()
        results[num_guesses] += 1
    pattern_cache._save_cache()
    entropy_cache._save_cache()
    end = datetime.now()
    print("Finished in {:.2f}s\n".format((end - start).seconds))

    for i in range(7):
        print("Guesses: {} -> {}".format(i, results[i]))

    print()
