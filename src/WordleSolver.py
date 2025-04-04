from collections import Counter
import random


class WordleSolver:
    def __init__(self, corpus):
        self.corpus = corpus
        print("0: Does not appear")
        print("1: Correct position")
        print("2: Incorrect position")

    def generateGuess(self):
        return random.choice(self.corpus)

    def processResult(self, guess, state):
        filtered_corpus = []

        for word in self.corpus:
            # Check if this word is compatible with our guess and state
            is_compatible = True

            # Track letters we've accounted for (to handle duplicate letters)
            letter_counts = Counter(word)

            # First pass: handle exact matches (state 1) and non-matches (state 0)
            for i, (guess_letter, status) in enumerate(zip(guess, state)):
                if status == 1:
                    # Letter must be in this position
                    if word[i] != guess_letter:
                        is_compatible = False
                        break
                    # Decrement the count as we've accounted for this letter
                    letter_counts[guess_letter] -= 1

            if not is_compatible:
                continue

            # Second pass: handle letters that exist but in wrong position (state 2)
            for i, (guess_letter, status) in enumerate(zip(guess, state)):
                if status == 2:
                    if word[i] == guess_letter:
                        is_compatible = False
                        break
                    if letter_counts.get(guess_letter, 0) <= 0:
                        is_compatible = False
                        break
                    letter_counts[guess_letter] -= 1
                elif status == 0:
                    # Letter shouldn't exist in the word (or all instances are accounted for)
                    # Count how many times this letter appears with status 1 or 2
                    accounted_for = sum(
                        1
                        for j, s in enumerate(state)
                        if (s == 1 or s == 2) and guess[j] == guess_letter
                    )

                    # If we have more of this letter in the word than accounted for, it's incompatible
                    if (
                        guess_letter in letter_counts
                        and letter_counts[guess_letter] > 0
                    ):
                        # There are unaccounted instances of this letter
                        is_compatible = False
                        break

            if is_compatible:
                filtered_corpus.append(word)

        self.corpus = filtered_corpus

    def remainingWords(self):
        return len(self.corpus)
