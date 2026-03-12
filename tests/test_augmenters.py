from tatk import (
    SynonymReplacementAugmenter,
    RandomDeletionAugmenter,
    RandomSwapAugmenter,
    RandomInsertionAugmenter,
    AugmentationPipeline,
)


def test_random_deletion_returns_string():
    aug = RandomDeletionAugmenter(p=0.2)
    result = aug.augment("This is a simple test sentence.")
    assert isinstance(result, str)
    assert len(result) > 0


def test_random_swap_returns_string():
    aug = RandomSwapAugmenter(n=2)
    result = aug.augment("This is another simple sentence.")
    assert isinstance(result, str)


def test_synonym_replacement_returns_string():
    aug = SynonymReplacementAugmenter(n=1)
    result = aug.augment("The quick brown fox jumps over the lazy dog.")
    assert isinstance(result, str)


def test_random_insertion_returns_string():
    aug = RandomInsertionAugmenter(n=1)
    result = aug.augment("The model performed well on the validation set.")
    assert isinstance(result, str)


def test_pipeline_augment_many_length():
    pipeline = AugmentationPipeline(
        augmenters=[RandomSwapAugmenter(n=1)],
        sequential=True,
    )
    results = pipeline.augment_many("Testing the pipeline.", n=3)
    assert len(results) == 3