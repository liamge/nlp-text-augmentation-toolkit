import random
import re
from typing import List

TOKEN_PATTERN = re.compile(r"\w+|[^\w\s]")

def tokenize(text: str) -> List[str]:
    """
    Simple tokenizer that preserves punctuation as separate tokens.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return TOKEN_PATTERN.findall(text)


def detokenize(tokens: List[str]) -> str:
    """
    Reconstruct text from tokens with basic punctuation handling.
    """
    text = " ".join(tokens)
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    return text.strip()


def is_word(token: str) -> bool:
    return token.isalpha()


def safe_sample(items: List[str], k: int) -> List[str]:
    if not items:
        return []
    k = min(k, len(items))
    return random.sample(items, k)


def set_seed(seed: int) -> None:
    random.seed(seed)