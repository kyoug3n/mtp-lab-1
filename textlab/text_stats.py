"""Простая статистика по тексту: количество слов и средняя длина слова."""

import re

WORD_PATTERN = re.compile(r"[a-zа-яё0-9]+", re.IGNORECASE)


def words(text: str) -> list[str]:
    """Разбить текст на слова в нижнем регистре."""
    return WORD_PATTERN.findall(text.lower())


def word_count(text: str) -> int:
    """Вернуть количество слов в тексте."""
    return len(words(text))


def average_word_length(text: str) -> float:
    """Вернуть среднюю длину слова в тексте; для пустого текста — 0.0."""
    items = words(text)
    if not items:
        return 0.0
    return sum(len(item) for item in items) / len(items)
