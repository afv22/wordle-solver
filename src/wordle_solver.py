import math
import random

from collections import Counter, defaultdict

from .cache import Cache
from .pattern import Pattern
from .utils import Color, Criteria


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
        self.expected_value_cache = {}
        self.entropy_cache = entropy_cache or Cache("entropy_cache.pkl")
        self.pattern_cache = pattern_cache or Cache("pattern_cache.pkl")

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

    def generate_guess(self, guesses_made) -> tuple[str, int]:
        """Generate the next optimal guess based on the selected criteria"""
        if self.selection_criteria == Criteria.RANDOM:
            return (random.choice(self.corpus), 0)

        if self.selection_criteria == Criteria.ENTROPY:
            if guesses_made == 0:
                return ("tares", self._calculate_entropy("tares"))

            n = self.remainingWords()
            if n <= 2:
                return (self.corpus[0], 1.0)

            # If in the endgame and there is only one differing letter in all remaining
            # possibilities, find a word that uses as many of those letters as possible.
            # If it's the last guess however, there is no point in doing this.
            if n <= 10 and guesses_made < 5:
                i = self._last_unspecified_index()
                if i >= 0:
                    return self._generate_endgame_guess(i)

            corpus_key = frozenset(self.corpus)
            if corpus_key in self.entropy_cache:
                return self.entropy_cache[corpus_key]

            # Find word with maximum entropy
            return self._generate_entropy_guess(corpus_key)

        if self.selection_criteria == Criteria.EXPECTED_MOVES:
            if guesses_made == 0:
                # TODO: Calculate optimal guess for this strategy
                return ("tares", self._calculate_entropy("tares"))
            return self._lowest_expected_number_of_moves(self.corpus)

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

    def _lowest_expected_number_of_moves(self, words):
        key = frozenset(words)
        if key in self.expected_value_cache:
            return self.expected_value_cache[key]
            
        n = len(words)

        if n == 1:
            return (words[0], 1)

        optimal_guess = None
        optimal_expected_guesses = float("inf")

        for guess in words:
            pattern_counts = defaultdict(list)
            for answer in words:
                pattern = self._get_pattern(guess, answer)
                pattern_counts[pattern].append(answer)

            expected_value = 0
            for possible_answers in pattern_counts.values():
                _, pattern_expected_value = self._lowest_expected_number_of_moves(
                    possible_answers
                )
                prob = len(possible_answers) / n
                expected_value += pattern_expected_value * prob

            if expected_value < optimal_expected_guesses:
                optimal_expected_guesses = expected_value
                optimal_guess = guess

        value = (optimal_guess, optimal_expected_guesses + 1)
        self.expected_value_cache[key] = value
        return value

    def get_uncertainty(self):
        return math.log(len(self.corpus), 2)