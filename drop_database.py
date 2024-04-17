"""Модуль для удаления данных и таблиц из бд."""

from migrate import execute_command

TABLES = (
    "product",
    "ordert",
    "rack",
    "rack_product_link",
    "order_product_link",
)


def drop() -> None:
    """Основная функция модуля."""
    for table in TABLES:
        sql_command = f"DROP TABLE IF EXISTS {table} CASCADE"
        execute_command(sql_command)


if __name__ == "__main__":
    drop()
