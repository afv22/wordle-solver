from collections import Counter, defaultdict
import random
import math
import pickle
import os

from .colors import Color
from .guess_criteria import Criteria


class WordleSolver:
    CACHE_FILE = "entropy_cache.pkl"

    def __init__(self, corpus, criteria=Criteria.ENTROPY):
        self.corpus = corpus
        self.selection_criteria = criteria
        self.pattern_cache = {}  # Cache for word-pattern compatibility
        self.entropy_cache = {}  # Cache for word entropy values
        self._load_entropy_cache()

    def _load_entropy_cache(self) -> None:
        """Load precomputed entropy values from file if available."""
        if os.path.exists(self.CACHE_FILE):
            try:
                with open(self.CACHE_FILE, "rb") as f:
                    self.entropy_cache = pickle.load(f)
            except Exception:
                pass

    def _save_entropy_cache(self) -> None:
        """Save computed entropy values to file."""
        try:
            with open(self.CACHE_FILE, "wb") as f:
                pickle.dump(self.entropy_cache, f)
        except Exception:
            pass

    def generateGuess(self) -> tuple[str, int]:
        """Generate the next optimal guess based on the selected criteria."""
        if self.selection_criteria == Criteria.RANDOM:
            return random.choice(self.corpus)

        if self.selection_criteria == Criteria.ENTROPY:
            # Use precomputed values for the initial guess (when corpus is full size)
            corpus_key = frozenset(self.corpus)
            if corpus_key in self.entropy_cache:
                return self.entropy_cache[corpus_key]

            # Find word with maximum entropy
            max_entropy = -1
            optimal_word = None

            for word in self.corpus:
                word_cache_key = (word, corpus_key)
                if word_cache_key in self.entropy_cache:
                    entropy = self.entropy_cache[word_cache_key]
                else:
                    entropy = self._calculate_entropy(word)
                    self.entropy_cache[word_cache_key] = entropy

                if entropy > max_entropy:
                    max_entropy = entropy
                    optimal_word = word

            # Save cache periodically
            if len(self.corpus) > 1000:  # Only save for initial calculations
                self._save_entropy_cache()

            return (optimal_word, max_entropy)

    def processResult(self, guess, pattern) -> None:
        self.corpus = [
            word
            for word in self.corpus
            if self._is_word_compatible(word, guess, pattern)
        ]

    def _is_word_compatible(self, word, guess, pattern) -> bool:
        letter_counts = Counter(word)

        # First pass: check green letters (exact matches)
        for i, letter in enumerate(guess):
            if pattern[i] == Color.GREEN:
                if word[i] != letter:
                    return False
                letter_counts[letter] -= 1

        # Second pass: check yellow and grey letters
        for i, letter in enumerate(guess):
            if pattern[i] == Color.YELLOW:
                # Letter exists but not in this position
                if word[i] == letter:
                    return False
                if letter_counts.get(letter, 0) <= 0:
                    return False
                letter_counts[letter] -= 1

            elif pattern[i] == Color.GREY:
                # If we have unaccounted instances of this letter, it's incompatible
                if letter_counts[letter] > 0:
                    return False

        return True

    def _calculate_entropy(self, word) -> float:
        """Calculate entropy for a word using optimized methods."""
        corpus_size = len(self.corpus)

        # Use a pattern frequency dictionary instead of calculating all matches
        pattern_freqs = defaultdict(int)

        # For each word in corpus, determine what pattern would result
        for candidate in self.corpus:
            pattern = self._get_pattern(word, candidate)
            pattern_freqs[pattern] += 1

        # Calculate entropy from pattern frequencies
        entropy = 0
        for count in pattern_freqs.values():
            prob = count / corpus_size
            entropy += prob * math.log2(1 / prob)

        return entropy

    def _get_pattern(self, guess, answer) -> tuple:
        """Get the color pattern when 'guess' is played against 'answer'."""
        pattern = [Color.GREY] * len(guess)

        # First pass: mark green matches
        letter_counts = Counter(answer)
        for i, (g, a) in enumerate(zip(guess, answer)):
            if g == a:
                pattern[i] = Color.GREEN
                letter_counts[g] -= 1

        # Second pass: mark yellow matches
        for i, (g, p) in enumerate(zip(guess, pattern)):
            if p == Color.GREY and letter_counts.get(g, 0) > 0:
                pattern[i] = Color.YELLOW
                letter_counts[g] -= 1

        return tuple(pattern)

    def remainingWords(self) -> int:
        return len(self.corpus)
