"""Модуль входа в программу."""

from database import Database
from settings import settings


def main() -> None:
    """Главная функция."""
    db = Database(settings=settings)
    with db() as conn:
        conn.cursor()


if __name__ == "__main__":
    main()
