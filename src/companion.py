import math
import random

from collections import Counter, defaultdict

from .cache import Cache
from .pattern import Pattern, pattern_utils
from .utils import Color, Criteria, load_wordlist


class Companion:
    def __init__(
        self,
        corpus: list[str],
        criteria: Criteria,
    ):
        self.full_corpus = corpus
        self.possible_guesses = []
        self.selection_criteria = criteria
        self.entropy_cache = Cache("entropy_cache.pkl")
        freqs = load_wordlist("wordlists/five_letter_freq.csv")
        self.word_frequencies = {}
        for index, (word, count, normalized_count) in freqs.iterrows():
            self.word_frequencies[word] = normalized_count

    def _sort_possible_guesses(self) -> None:
        new_possible_guesses = []
        curr_possible_guesses = [guess for _, guess in self.possible_guesses]
        for _, guess in self.possible_guesses:
            if self.selection_criteria == Criteria.ENTROPY:
                ranking = self._calculate_entropy(guess)
            elif self.selection_criteria == Criteria.EXPECTED_MOVES:
                ranking = self._expected_moves(guess, curr_possible_guesses)
            elif self.selection_criteria == Criteria.RANDOM:
                ranking = random.randrange(len(self.possible_guesses))
            new_possible_guesses.append((ranking, guess))

        new_possible_guesses.sort()
        self.possible_guesses = new_possible_guesses

    def reset(self) -> None:
        self.possible_guesses = [(0, word) for word in self.full_corpus]

    def _last_unspecified_index(self) -> int:
        """If all remaining words differ by only one letter, return the index"""
        """of that unknown letter. Otherwise, return -1"""
        words = [word for _, word in self.possible_guesses]
        index = None
        for i in range(5):
            if len(set([word[i] for word in words])) > 1:
                if index != None:
                    return -1
                index = i
        return index

    def _generate_endgame_guess(self, i: int) -> tuple[str, int]:
        letters = [word[i] for _, word in self.possible_guesses]
        max_represented_letters = 0
        optimal_word = None
        for word in self.full_corpus:
            represented_letters = sum(1 for c in letters if c in word)
            if represented_letters > max_represented_letters:
                max_represented_letters = represented_letters
                optimal_word = word
        return optimal_word

    def generate_guess(self, round: int) -> str:
        """Generate the next optimal guess based on the selected criteria"""
        if not self.possible_guesses:
            raise ValueError("No remaining possible words")

        if round == 1:
            # TODO: Generate initial state for each strategy
            return "tares"

        # If in the endgame and there is only one differing letter in
        # all remaining possibilities, find a word that uses as many of
        # those letters as possible. If it's the last guess however,
        # there is no point in doing this.
        if 2 < self.remaining_words() <= 10 and round < 6:
            i = self._last_unspecified_index()
            if i >= 0:
                return self._generate_endgame_guess(i)

        return self.possible_guesses[0][1]

    def process_result(self, guess, pattern: Pattern) -> None:
        """Filter remaining corpus according to the given pattern and sort"""
        self.possible_guesses = [
            (rank, word)
            for rank, word in self.possible_guesses
            if self._is_word_compatible(word, guess, pattern)
        ]
        self._sort_possible_guesses()

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
        corpus_size = len(self.possible_guesses)

        # Use a pattern frequency dictionary instead of calculating all matches
        pattern_freqs = defaultdict(int)

        # For each word in corpus, determine what pattern would result
        for _, candidate in self.possible_guesses:
            pattern = pattern_utils.calculate_from_guess(word, candidate)
            pattern_freqs[pattern] += 1

        # Calculate entropy from pattern frequencies
        entropy = 0
        for count in pattern_freqs.values():
            prob = count / corpus_size
            entropy += prob * math.log2(1 / prob)

        return -entropy

    def remaining_words(self) -> int:
        return len(self.possible_guesses)

    def _expected_moves(self, guess: str, words: list[str]):
        if len(words) == 1:
            return self.word_frequencies.get([words[0]], 0)

        pattern_counts = defaultdict(list)
        for answer in words:
            pattern = pattern_utils.calculate_from_guess(guess, answer)
            pattern_counts[pattern].append(answer)

        guess_expected_moves = 1
        for possible_answers in pattern_counts.values():
            answer_probability = 1 / len(possible_answers)
            pattern_expected_moves = 0

            for answer in possible_answers:
                expected_moves = self._expected_moves(answer, possible_answers)
                pattern_expected_moves += expected_moves * answer_probability

            pattern_probability = len(possible_answers) / len(words)
            guess_expected_moves += pattern_expected_moves * pattern_probability

        return guess_expected_moves

    def get_uncertainty(self):
        """Calculate the remaining uncertainty in the possible words, in bits"""
        return math.log(len(self.possible_guesses), 2)
