"""Тесты модуля textlab.text_stats."""

import unittest

from textlab import text_stats


class WordsTest(unittest.TestCase):
    def test_splits_and_lowercases(self) -> None:
        self.assertEqual(text_stats.words("Привет, Git!"), ["привет", "git"])

    def test_empty_text(self) -> None:
        self.assertEqual(text_stats.words(""), [])


class WordCountTest(unittest.TestCase):
    def test_counts_words(self) -> None:
        self.assertEqual(text_stats.word_count("один два, три"), 3)


class AverageWordLengthTest(unittest.TestCase):
    def test_average(self) -> None:
        self.assertEqual(text_stats.average_word_length("ab abcd"), 3.0)

    def test_empty_text_returns_zero(self) -> None:
        self.assertEqual(text_stats.average_word_length(""), 0.0)


if __name__ == "__main__":
    unittest.main()
