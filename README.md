# TATK — Text Augmentation Toolkit

A lightweight Python package for NLP data augmentation.

## Features

- Synonym replacement
- Random deletion
- Random swap
- Random insertion
- Augmentation pipelines
- Back-translation interface

## Installation

```bash
pip install -r requirements.txt
```

## NLTK Setup

```
import nltk
nltk.download("wordnet")
nltk.download("omw-1.4")
```

## Example

```
from tatk import SynonymReplacementAugmenter, AugmentationPipeline

pipeline = AugmentationPipeline(
    augmenters=[SynonymReplacementAugmenter(n=2)]
)

text = "The product quality was excellent and the delivery was fast."
print(pipeline.augment(text))
```