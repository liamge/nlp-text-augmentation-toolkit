import random
from typing import List, Optional

from .augmenters import BaseAugmenter


class AugmentationPipeline:
    """
    Apply one or more augmenters in sequence or sample one at random.
    """

    def __init__(
        self,
        augmenters: List[BaseAugmenter],
        sequential: bool = True,
        augmentation_prob: float = 1.0,
    ):
        if not augmenters:
            raise ValueError("augmenters must not be empty")
        if not 0 <= augmentation_prob <= 1:
            raise ValueError("augmentation_prob must be between 0 and 1")

        self.augmenters = augmenters
        self.sequential = sequential
        self.augmentation_prob = augmentation_prob

    def augment(self, text: str) -> str:
        if random.random() > self.augmentation_prob:
            return text

        if self.sequential:
            output = text
            for augmenter in self.augmenters:
                output = augmenter.augment(output)
            return output

        augmenter = random.choice(self.augmenters)
        return augmenter.augment(text)

    def augment_many(self, text: str, n: int = 5) -> List[str]:
        return [self.augment(text) for _ in range(n)]