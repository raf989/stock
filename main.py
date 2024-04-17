"""Модуль входа в программу."""

import argparse

from view import View


def main() -> None:
    """Главная функция."""
    parser = argparse.ArgumentParser()
    parser.add_argument("orders", type=str, help="1,2,3")
    orders = parser.parse_args().orders
    v = View(orders.split(","))
    print(v)


if __name__ == "__main__":
    main()
