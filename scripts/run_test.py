import random
import sys

from collections import Counter
from datetime import datetime
from tqdm import tqdm

from src import Cache, Wordle, WordleSolver, load_wordlist
from .utils import get_strategy


def main(iterations=10, filepath="wordlists/wordlist.txt"):
    strategy = get_strategy()

    print("Loading wordlist...")
    corpus = load_wordlist(filepath)['word'].to_list()

    print("Running benchmarker...")
    start = datetime.now()

    results = Counter()
    entropy_cache = Cache("entropy_cache.pkl")
    pattern_cache = Cache("pattern_cache.pkl")
    for _ in tqdm(range(iterations), ncols=80):
        answer = random.choice(corpus)
        wordle = Wordle(answer)
        solver = WordleSolver(corpus, strategy, entropy_cache, pattern_cache)
        while wordle.is_active():
            guess, _ = solver.generate_guess(wordle.guesses_made)
            pattern = wordle.process_guess(guess)
            solver.process_result(guess, pattern)
        num_guesses = len(wordle.guesses) if wordle.has_won else 0
        results[num_guesses] += 1

    pattern_cache._save_cache()
    entropy_cache._save_cache()
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
