import random
import sys

from collections import Counter
from datetime import datetime
from tqdm import tqdm

from src import Cache, Criteria, Wordle, WordleSolver, load_wordlist

def get_strategy():
    print("Select your strategy:")
    print("1) Random")
    print("2) Entropy")
    print("3) Expected Value")
    
    criteria_choice = input("> ")
    while criteria_choice not in ["1", "2", "3"]:
        print("Try again.")
        criteria_choice = input("> ")

    if criteria_choice == "1":
        criteria = Criteria.RANDOM
    elif criteria_choice == "2":
        criteria = Criteria.ENTROPY
    elif criteria_choice == "3":
        criteria = Criteria.EXPECTED_MOVES
    else:
        raise ValueError("Invalid Criteria Selection")

    return criteria


def main(iterations=10, filepath='wordlists/wordlist.txt'):
    strategy = get_strategy()

    print("Loading wordlist...")
    corpus = load_wordlist(filepath)

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
        num_guesses = wordle.guesses_made if wordle.has_won else 0
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