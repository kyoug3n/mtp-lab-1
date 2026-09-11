"""Точка входа учебного проекта."""


def greet(name: str) -> str:
    """Вернуть приветствие для указанного имени."""
    return f"Привет, {name}!"


def main() -> None:
    """Вывести приветствие."""
    print(greet("Git"))


if __name__ == "__main__":
    main()
