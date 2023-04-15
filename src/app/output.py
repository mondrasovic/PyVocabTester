from __future__ import annotations

import abc
import textwrap
from typing import TYPE_CHECKING

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from app.exam import VocabularyExamData

if TYPE_CHECKING:
    pass


class ExamTextOutputGenerator(abc.ABC):
    @abc.abstractmethod
    def generate_output(self, exam_data: VocabularyExamData) -> None:
        pass


class ConsoleOutputGenerator(ExamTextOutputGenerator):
    def __init__(self) -> None:
        super().__init__()

        colorama_init()

    def generate_output(self, exam_data: VocabularyExamData) -> None:
        text_with_blanks = textwrap.fill(exam_data.text_with_blanks)
        suggested_terms_text = textwrap.fill(
            ", ".join(
                term for term in sorted(exam_data.correct_answers.values())
            )
        )
        correct_answers_text = "\n".join(
            f"{key} - {correct_answer}" for key, correct_answer in
            sorted(exam_data.correct_answers.items())
        )

        output_text = f"""{Fore.RED}Vocabulary Practice - Fill In the Blanks{Fore.RESET}

{text_with_blanks}

{Fore.RED}Suggested Answers{Fore.RESET}
{Fore.BLUE}{suggested_terms_text}{Fore.RESET}

----------------------------------------------------------------------

{Fore.RED}Correct Answers{Fore.RED}
{Fore.GREEN}{correct_answers_text}{Fore.RESET}
"""
        print(output_text)
