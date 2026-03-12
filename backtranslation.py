from abc import ABC, abstractmethod


class BaseTranslator(ABC):
    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        raise NotImplementedError


class BackTranslationAugmenter:
    """
    Generic back translation wrapper.

    You can later plug in:
    - MarianMT
    - Google Translate API
    - DeepL
    - OpenAI-based translation workflow
    """

    def __init__(self, translator: BaseTranslator, pivot_lang: str = "fr"):
        self.translator = translator
        self.pivot_lang = pivot_lang

    def augment(self, text: str, source_lang: str = "en") -> str:
        intermediate = self.translator.translate(
            text=text,
            source_lang=source_lang,
            target_lang=self.pivot_lang,
        )
        return self.translator.translate(
            text=intermediate,
            source_lang=self.pivot_lang,
            target_lang=source_lang,
        )