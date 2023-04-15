import re
import pytest

from app.exam import get_term_raw_regex, expunge_terms_numbered, normalize_correct_answers


class TestExamPracticeTextGenerating:
    BLANK_WORD = "___"

    @pytest.mark.parametrize(
        "term, text, is_valid",
        [
            # Positive test cases
            pytest.param("word", "word", True, id="exact_match"),
            pytest.param("word", "WoRd", True, id="letter_case_variation"),
            pytest.param("word", "    word  ", True, id="enclosing_whitespace"),
            pytest.param("word", "   word?", True, id="question_mark"),
            pytest.param("word", "   word!", True, id="exclamation_mark"),
            pytest.param("word", "   word,", True, id="comma"),
            pytest.param("word", "   word.", True, id="period"),
            pytest.param(
                "multi word", "   multi word.", True, id="multiple_words"
            ),
            # Negative test cases
            pytest.param("word", "words", False, id="word_prefix"),
            pytest.param("thing", "something", False, id="word_suffix"),
            pytest.param("word", "...words...", False, id="enclosing_dots"),
        ]
    )
    def test_get_term_raw_regex_search(self, term, text, is_valid):
        regex = get_term_raw_regex(term)
        assert (re.search(regex, text, re.IGNORECASE) is not None) == is_valid

    @pytest.mark.parametrize(
        "vocabulary, text, expected_text_with_blanks, expected_correct_answers",
        [
            pytest.param(
                [],
                "One little, two little, three little indians.",
                "One little, two little, three little indians.", {},
                id="empty_vocabulary"
            ),
            pytest.param(
                ["one", "two", "three"],
                "One little, two little, three little indians.",
                "(A)___ little, (B)___ little, (C)___ little indians.", {
                    "A": "ONE",
                    "B": "TWO",
                    "C": "THREE"
                },
                id="three_basic_terms"
            ),
            pytest.param(
                ["stick to your guns"],
                "It is of paramount importance to stick to your guns!",
                "It is of paramount importance to (A)___!",
                {"A": "STICK TO YOUR GUNS"},
                id="multi-word_terms"
            ),
            pytest.param(
                ["on the spur of the moment"],
                "And then, on the\nspur of the moment, I realized that...",
                "And then, (A)___, I realized that...",
                {"A": "ON THE SPUR OF THE MOMENT"},
                id="terms_span_multiple_lines"
            ),
            pytest.param(
                ["thing", "one"],
                "Someone told me one thing about something!",
                "Someone told me (A)___ (B)___ about something!", {
                    "A": "ONE",
                    "B": "THING"
                },
                id="terms_prefix_suffix"
            ),
        ]
    )
    def test_expunge_vocabulary_numbered(
        self, vocabulary, text, expected_text_with_blanks,
        expected_correct_answers
    ):
        exam_text = expunge_terms_numbered(text, vocabulary, self.BLANK_WORD)
        assert exam_text.original_text == text
        assert exam_text.text_with_blanks == expected_text_with_blanks
        assert exam_text.correct_answers == expected_correct_answers

    @pytest.mark.parametrize(
        "correct_answers, expected_normalized_correct_answers", [
            pytest.param(
                {
                    "A": "one",
                    "B": "two",
                    "C": "three"
                }, {
                    "A": "ONE",
                    "B": "TWO",
                    "C": "THREE"
                },
                id="basic_words"
            ),
            pytest.param(
                {"X": "at the drop of a hat"}, {"X": "AT THE DROP OF A HAT"},
                id="multi-word_item"
            ),
            pytest.param(
                {"key": "split\nhairs"}, {"key": "SPLIT HAIRS"},
                id="multi-line_item"
            ),
        ]
    )
    def test_normalize_correct_answers(
        self, correct_answers, expected_normalized_correct_answers
    ):
        normalized_correct_answers = normalize_correct_answers(correct_answers)
        assert normalized_correct_answers == expected_normalized_correct_answers
