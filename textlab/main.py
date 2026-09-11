"""Точка входа учебного проекта."""

import platform
from datetime import date


def greet(name: str) -> str:
    """Вернуть приветствие для указанного имени."""
    return f"Привет, {name}!"


def environment_info() -> str:
    """Вернуть строку с текущей датой и версией интерпретатора Python."""
    return f"Дата: {date.today():%d.%m.%Y}, Python {platform.python_version()}"


def main() -> None:
    """Вывести приветствие и сведения об окружении."""
    print(greet("Git"))
    print(environment_info())


if __name__ == "__main__":
    main()
