import random
from collections import defaultdict

class BigramModel:
    def __init__(self, corpus):
        self.bigram_probs = self.build_bigram_model(corpus)

    def build_bigram_model(self, corpus):
        bigram_counts = defaultdict(lambda: defaultdict(int))

        for sentence in corpus:
            words = sentence.lower().split()
            for i in range(len(words) - 1):
                w1, w2 = words[i], words[i+1]
                bigram_counts[w1][w2] += 1

        # convert counts → probabilities
        bigram_probs = {}
        for w1, next_words in bigram_counts.items():
            total = sum(next_words.values())
            bigram_probs[w1] = {w2: count / total for w2, count in next_words.items()}

        return bigram_probs

    def generate_text(self, start_word, length):
        start_word = start_word.lower()
        if start_word not in self.bigram_probs:
            return f"Start word '{start_word}' not found in corpus."

        result = [start_word]
        current_word = start_word

        for _ in range(length - 1):
            next_words = self.bigram_probs.get(current_word, {})
            if not next_words:
                break

            # weighted random choice
            words = list(next_words.keys())
            probs = list(next_words.values())
            current_word = random.choices(words, probs)[0]
            result.append(current_word)

        return " ".join(result)
