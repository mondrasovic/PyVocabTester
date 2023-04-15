from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable


class EnglishPracticeGPTPromptGenerator:
    def __init__(
        self,
        vocabulary: Iterable[str],
        n_used_terms: int,
        n_output_words: int = 80,
        allow_repetition: bool = False
    ) -> None:
        self.vocabulary = list(vocabulary)
        self.n_used_terms = n_used_terms
        self.n_output_words = n_output_words
        self.allow_repetition = allow_repetition

    def generate(self) -> str:
        term_repetition_query = "Each term from the given vocabulary "
        if self.allow_repetition:
            term_repetition_query += "may be used more than once."
        else:
            term_repetition_query += "should be used exactly once."

        n_terms_to_use = min(self.n_used_terms, len(self.vocabulary))
        vocabulary_items = "\n".join(
            f"- {vocabulary_item}" for vocabulary_item in
            random.sample(population=self.vocabulary, k=n_terms_to_use)
        )

        return f"""Create a coherent English text containing approxiatemly {self.n_output_words} that contains the following terms listed below:
{vocabulary_items}
{term_repetition_query}
"""
