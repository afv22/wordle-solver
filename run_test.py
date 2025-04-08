import random
import sys

from collections import Counter
from datetime import datetime
from tqdm import tqdm

from src import Cache, Criteria, Wordle, WordleSolver, load_wordlist

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 1:
        iterations = int(args[0])
        wordlist_filepath = args[1]
    else:
        iterations = 10
        wordlist_filepath = args[0]

    print("Loading wordlist...")
    corpus = load_wordlist(wordlist_filepath)

    print("Running benchmarker...")
    start = datetime.now()

    results = Counter()
    entropy_cache = Cache("entropy_cache.pkl")
    pattern_cache = Cache("pattern_cache.pkl")
    for _ in tqdm(range(iterations), ncols=80):
        answer = random.choice(corpus)
        wordle = Wordle(answer)
        solver = WordleSolver(corpus, Criteria.EXPECTED_MOVES, entropy_cache, pattern_cache)
        while wordle.is_active():
            guess, _ = solver.generate_guess(wordle.guesses_made)
            pattern = wordle.process_guess(guess)
            solver.process_result(guess, pattern)
        num_guesses = wordle.guesses_made if wordle.has_won else 0
        results[num_guesses] += 1

    pattern_cache._save_cache()
    entropy_cache._save_cache()
    end = datetime.now()
    print("Finished in {:.2f}s\n".format((end - start).seconds))

    for i in range(7):
        print("Guesses: {} -> {}".format(i, results[i]))

    print()
