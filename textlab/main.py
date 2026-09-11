"""Точка входа учебного проекта."""

import platform
from datetime import date

from textlab import text_stats

SAMPLE_TEXT = (
    "Git хранит историю проекта, а ветки позволяют вести работу параллельно."
)


def greet(name: str) -> str:
    """Вернуть приветствие для указанного имени."""
    return f"Привет, {name}!"


def environment_info() -> str:
    """Вернуть строку с текущей датой и версией интерпретатора Python."""
    return f"Дата: {date.today():%d.%m.%Y}, Python {platform.python_version()}"


def main() -> None:
    """Вывести приветствие, сведения об окружении и статистику текста."""
    print(greet("Git"))
    print(environment_info())
    print(f"Слов в примере: {text_stats.word_count(SAMPLE_TEXT)}")
    average = text_stats.average_word_length(SAMPLE_TEXT)
    print(f"Средняя длина слова: {average:.2f}")


if __name__ == "__main__":
    main()
