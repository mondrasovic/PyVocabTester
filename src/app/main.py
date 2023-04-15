from __future__ import annotations

import argparse
from typing import TYPE_CHECKING
from app.output import ConsoleOutputGenerator
from app.exam import VocabularyExamData

if TYPE_CHECKING:
    pass

def main() -> None:
    text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec vestibulum risus. Quisque eu ultricies ex. Aenean sit amet erat id dolor dictum lobortis. Duis bibendum elit in ipsum eleifend, eu pulvinar libero bibendum. Nulla facilisi. Sed pellentesque quam vel risus dapibus iaculis. Sed fringilla ut augue id ullamcorper. Sed molestie massa sit amet urna facilisis, at tristique mi finibus. Vestibulum quis tellus blandit, efficitur quam non, hendrerit ante. Vivamus ac augue a leo facilisis sagittis id eget arcu. Nullam cursus elit ac quam elementum consequat. In feugiat sapien non enim pretium, non molestie justo sagittis. Sed sit amet lorem nulla. Fusce sed placerat tellus, a posuere tellus. Nam nec mauris et nisl ultricies commodo in eu justo. Nulla tristique tellus a libero commodo, id iaculis arcu semper. Morbi scelerisque, magna sed molestie pellentesque, velit velit interdum mi, eget consequat ante lacus a nisi."""
    correct_answers = {
        "B": "first",
        "C": "second"
    }
    exam_data = VocabularyExamData("", text_with_blanks=text, correct_answers=correct_answers)
    ConsoleOutputGenerator().generate_output(exam_data)


if __name__ == "__main__":
    main()
