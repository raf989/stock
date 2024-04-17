"""Скрипт для миграциии таблиц в актульную базу данных."""

from database import Database
from settings import settings

db = Database(settings=settings)


def execute_command(sql_command: str) -> None:
    """Функция для исполнения sql-скриптов.

    Args:
    ----
        sql_command (str): sql-скрипт

    """
    with db() as conn:
        cur = conn.cursor()
        cur.execute(sql_command)
        conn.commit()


product_table_create = """
CREATE TABLE IF NOT EXISTS product (
id SERIAL PRIMARY KEY,
name VARCHAR(50) NOT NULL,
article INTEGER UNIQUE NOT NULL
)
"""
rack_table_create = """
CREATE TABLE IF NOT EXISTS rack (
id SERIAL PRIMARY KEY,
name VARCHAR(5) UNIQUE NOT NULL
)
"""
order_table_create = """
CREATE TABLE IF NOT EXISTS ordert (
id SERIAL PRIMARY KEY,
order_number INTEGER UNIQUE NOT NULL,
consumer_name VARCHAR(50) NOT NULL
)
"""
rack_product_link_create = """
CREATE TABLE IF NOT EXISTS rack_product_link (
id SERIAL PRIMARY KEY,
rack_id INTEGER NOT NULL,
product_id INTEGER NOT NULL,
main BOOLEAN NOT NULL,

CONSTRAINT FK_link_rack_product FOREIGN KEY(rack_id)
REFERENCES rack(id),

CONSTRAINT FK_link_product_rack FOREIGN KEY(product_id)
REFERENCES product(id)
)
"""
order_product_link_create = """
CREATE TABLE IF NOT EXISTS order_product_link (
id SERIAL PRIMARY KEY,
order_id INTEGER NOT NULL,
product_id INTEGER NOT NULL,
count INTEGER NOT NULL,

CONSTRAINT FK_link_order_product FOREIGN KEY(order_id)
REFERENCES ordert(id),

CONSTRAINT FK_link_product_order FOREIGN KEY(product_id)
REFERENCES product(id)
)
"""


def migrate() -> None:
    """Основная функция модуля."""
    execute_command(product_table_create)
    execute_command(rack_table_create)
    execute_command(order_table_create)
    execute_command(order_product_link_create)
    execute_command(rack_product_link_create)


if __name__ == "__main__":
    migrate()
