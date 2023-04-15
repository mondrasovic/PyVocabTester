from __future__ import annotations

import dataclasses
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Sequence, Mapping


@dataclasses.dataclass(frozen=True)
class VocabularyExamData:
    original_text: str
    text_with_blanks: str
    correct_answers: dict[str, str]


def expunge_terms_numbered(
    text: str,
    vocabulary: Sequence[str],
    blank_string: str = "___"
) -> VocabularyExamData:
    if not vocabulary:
        return VocabularyExamData(
            original_text=text, text_with_blanks=text, correct_answers={}
        )

    single_term_patterns = (get_term_raw_regex(item) for item in vocabulary)
    term_replace_patterns = re.compile(
        "|".join(single_term_patterns), re.IGNORECASE | re.MULTILINE
    )

    n_terms_replaced = 0
    correct_answers = {}

    def match_func(regex_match):
        nonlocal n_terms_replaced
        blank_spot_letter = chr(ord("A") + n_terms_replaced)
        replaced_word = regex_match.group()
        correct_answers[blank_spot_letter] = replaced_word
        n_terms_replaced += 1
        return f"({blank_spot_letter}){blank_string}"

    text_with_blanks = term_replace_patterns.sub(match_func, text)
    normalized_correct_answers = normalize_correct_answers(correct_answers)

    return VocabularyExamData(
        text, text_with_blanks, normalized_correct_answers
    )


def get_term_raw_regex(term: str) -> str:
    term_tokens = rf"\s*".join(term.split())
    return rf"\b{term_tokens}\b"


def normalize_correct_answers(
    correct_answers: Mapping[str, str]
) -> dict[str, str]:
    return {
        key: " ".join(correct_answer.strip().upper().split())
        for key, correct_answer in correct_answers.items()
    }
