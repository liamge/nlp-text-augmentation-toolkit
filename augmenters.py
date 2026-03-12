import random
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from nltk.corpus import wordnet as wn

from .utils import tokenize, detokenize, is_word


class BaseAugmenter(ABC):
    @abstractmethod
    def augment(self, text: str) -> str:
        raise NotImplementedError


class SynonymReplacementAugmenter(BaseAugmenter):
    """
    Replace up to n words with WordNet synonyms.
    """

    def __init__(self, n: int = 1, min_token_length: int = 3):
        self.n = n
        self.min_token_length = min_token_length

    def _get_synonyms(self, word: str) -> List[str]:
        synonyms = set()
        for syn in wn.synsets(word):
            for lemma in syn.lemmas():
                candidate = lemma.name().replace("_", " ").lower()
                if candidate != word.lower() and " " not in candidate:
                    synonyms.add(candidate)
        return list(synonyms)

    def augment(self, text: str) -> str:
        tokens = tokenize(text)
        candidate_indices = [
            i for i, tok in enumerate(tokens)
            if is_word(tok) and len(tok) >= self.min_token_length
        ]

        if not candidate_indices:
            return text

        random.shuffle(candidate_indices)
        replaced = 0

        for idx in candidate_indices:
            synonyms = self._get_synonyms(tokens[idx])
            if synonyms:
                replacement = random.choice(synonyms)
                if tokens[idx][0].isupper():
                    replacement = replacement.capitalize()
                tokens[idx] = replacement
                replaced += 1
            if replaced >= self.n:
                break

        return detokenize(tokens)


class RandomDeletionAugmenter(BaseAugmenter):
    """
    Delete tokens with probability p, while preserving at least one word token.
    """

    def __init__(self, p: float = 0.1):
        if not 0 <= p <= 1:
            raise ValueError("p must be between 0 and 1")
        self.p = p

    def augment(self, text: str) -> str:
        tokens = tokenize(text)
        if len(tokens) <= 1:
            return text

        kept = [tok for tok in tokens if random.random() > self.p]

        if not kept:
            kept = [random.choice(tokens)]

        return detokenize(kept)


class RandomSwapAugmenter(BaseAugmenter):
    """
    Randomly swap token positions n times.
    """

    def __init__(self, n: int = 1):
        self.n = n

    def augment(self, text: str) -> str:
        tokens = tokenize(text)
        if len(tokens) < 2:
            return text

        tokens = tokens[:]
        for _ in range(self.n):
            i, j = random.sample(range(len(tokens)), 2)
            tokens[i], tokens[j] = tokens[j], tokens[i]

        return detokenize(tokens)


class RandomInsertionAugmenter(BaseAugmenter):
    """
    Insert synonyms of existing words n times.
    """

    def __init__(self, n: int = 1, min_token_length: int = 3):
        self.n = n
        self.min_token_length = min_token_length

    def _get_synonyms(self, word: str) -> List[str]:
        synonyms = set()
        for syn in wn.synsets(word):
            for lemma in syn.lemmas():
                candidate = lemma.name().replace("_", " ").lower()
                if candidate != word.lower() and " " not in candidate:
                    synonyms.add(candidate)
        return list(synonyms)

    def augment(self, text: str) -> str:
        tokens = tokenize(text)
        word_tokens = [tok for tok in tokens if is_word(tok) and len(tok) >= self.min_token_length]

        if not word_tokens:
            return text

        tokens = tokens[:]
        inserted = 0
        attempts = 0
        max_attempts = self.n * 5

        while inserted < self.n and attempts < max_attempts:
            word = random.choice(word_tokens)
            synonyms = self._get_synonyms(word)
            if synonyms:
                new_word = random.choice(synonyms)
                insert_idx = random.randint(0, len(tokens))
                tokens.insert(insert_idx, new_word)
                inserted += 1
            attempts += 1

        return detokenize(tokens)