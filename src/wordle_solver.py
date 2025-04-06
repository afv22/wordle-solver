from collections import Counter, defaultdict
import random
import math

from .cache import Cache
from .colors import Color
from .pattern import Pattern
from .guess_criteria import Criteria


class WordleSolver:
    def __init__(
        self,
        corpus: list[str],
        criteria: Criteria,
        entropy_cache: Cache = None,
        pattern_cache: Cache = None,
    ):
        self.full_corpus = corpus
        self.corpus = corpus
        self.selection_criteria = criteria
        self.entropy_cache = entropy_cache or Cache("entropy_cache.pkl")
        self.pattern_cache = pattern_cache or Cache("pattern_cache.pkl", 1000)

    def _last_unspecified_index(self) -> int:
        """If all remaining words differ by only one letter, return the index"""
        """of that unknown letter. Otherwise, return -1"""
        for i in range(5):
            chars_at_position_i = [word[i] for word in self.corpus]
            unique_chars = set(chars_at_position_i)
            same_at_all_other_positions = True
            for j in range(5):
                if j != i:
                    chars_at_position_j = [word[j] for word in self.corpus]
                    if len(set(chars_at_position_j)) > 1:
                        same_at_all_other_positions = False
                        break

            if same_at_all_other_positions and len(unique_chars) == len(self.corpus):
                return i

        return -1

    def _generate_endgame_guess(self, i: int) -> tuple[str, int]:
        letters = [word[i] for word in self.corpus]
        max_letters = 0
        optimal_word = None
        for word in self.full_corpus:
            n = sum(1 for c in letters if c in word)
            if n > max_letters:
                max_letters = n
                optimal_word = word
        return (optimal_word, self._calculate_entropy(word))
    
    def _generate_entropy_guess(self, corpus_key) -> tuple[str, int]:
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

        return (optimal_word, max_entropy)

    def generate_guess(self, guess_number) -> tuple[str, int]:
        """Generate the next optimal guess based on the selected criteria"""
        if self.selection_criteria == Criteria.RANDOM:
            return (random.choice(self.corpus), 0)

        if self.selection_criteria == Criteria.ENTROPY:
            if guess_number == 1:
                return ('tares', self._calculate_entropy('tares'))
            
            n = self.remainingWords()
            if n <= 2:
                return (self.corpus[0], 1.0)

            # If in the endgame and there is only one differing letter in all remaining
            # possibilities, find a word that uses as many of those letters as possible.
            # If it's the last guess however, there is no point in doing this.
            if n <= 10 and guess_number != 6:
                i = self._last_unspecified_index()
                if i >= 0:
                    return self._generate_endgame_guess(i)

            # Use precomputed values for the initial guess (when corpus is full size)
            corpus_key = frozenset(self.corpus)
            if corpus_key in self.entropy_cache:
                return self.entropy_cache[corpus_key]

            # Find word with maximum entropy
            return self._generate_entropy_guess(corpus_key)

    def process_result(self, guess, pattern: Pattern) -> None:
        """Filter remaining corpus according to the given pattern"""
        self.corpus = [
            word
            for word in self.corpus
            if self._is_word_compatible(word, guess, pattern)
        ]

    def _is_word_compatible(self, word, guess, pattern: Pattern) -> bool:
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
        """Calculate entropy for a given word"""
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
        """Get the color pattern when 'guess' is played against 'answer'"""
        key = frozenset([guess, answer])
        if key in self.pattern_cache:
            return self.pattern_cache[key]

        pattern = [Color.GREY] * len(guess)

        # First pass: mark green matches
        letter_counts = Counter(answer)
        for i, (g, a) in enumerate(zip(guess, answer)):
            if g == a:
                pattern[i] = Color.GREEN
                letter_counts[g] -= 1

        # Second pass: mark yellow matches
        for i, (g, p) in enumerate(zip(guess, pattern)):
            if p == Color.GREY and letter_counts[g] > 0:
                pattern[i] = Color.YELLOW
                letter_counts[g] -= 1

        pattern = tuple(pattern)
        self.pattern_cache[key] = pattern
        return pattern

    def remainingWords(self) -> int:
        return len(self.corpus)
