from tatk import (
    SynonymReplacementAugmenter,
    RandomDeletionAugmenter,
    RandomSwapAugmenter,
    RandomInsertionAugmenter,
    AugmentationPipeline,
)

text = "The customer was extremely unhappy with the delayed order and poor support."

pipeline = AugmentationPipeline(
    augmenters=[
        SynonymReplacementAugmenter(n=2),
        RandomSwapAugmenter(n=1),
        RandomDeletionAugmenter(p=0.05),
    ],
    sequential=True,
)

print("Original:")
print(text)
print("\nAugmented:")
print(pipeline.augment(text))

print("\nMultiple samples:")
for sample in pipeline.augment_many(text, n=5):
    print("-", sample)