"""Модуль для удаление данных и таблиц в бд."""

from migrate import execute_command

TABLES = (
    "product",
    "rack",
    "ordert",
    "rack_product_link",
    "order_product_link",
)


def drop() -> None:
    """основная функция модуля."""
    for table in TABLES:
        sql_command = f"DROP TABLE IF EXISTS {table} CASCADE"
        execute_command(sql_command)


if __name__ == "__main__":
    drop()
