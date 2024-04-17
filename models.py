"""Модуль c описанием моделей БД для работы приложения."""

from abc import ABC, abstractmethod
from typing import Literal

from database import Database
from settings import db


class BaseModel(ABC):
    """Базовый класс модели."""

    @staticmethod
    @abstractmethod
    def get_by(field: str, value: int | str) -> "BaseModel":
        """Метод для получения экземляра модели из базы.

        Args:
        ----
            field (str): название поля.
            value (int | str): значение поля.

        Returns:
        -------
            BaseModel: экземпляр модели из базы.

        """


class BaseModelLink(ABC):
    """Базовый класс модели связи."""

    @staticmethod
    @abstractmethod
    def get_all_by(field: str, value: int | str) -> list["BaseModel"]:
        """Метод для получения экземляра модели из базы.

        Args:
        ----
            field (str): название поля.
            value (int | str): значение поля.

        Returns:
        -------
            list[BaseModel]: список соответствующих экземпляров модели из базы.

        """


class Rack(BaseModel):
    """Класс, представлющий стеллаж."""

    db: Database = db

    def __init__(self: "Rack", id_: int, name: str) -> None:
        """Конструктор.

        Args:
        ----
            self (Rack): сам экземпляр.
            id_ (int): id из базы.
            name (str): name из базы.

        """
        self.id = id_
        self.name = name

    @staticmethod
    def get_by(field: Literal["id", "name"], value: int | str) -> "Rack":
        """Получить по названию поля и значению запись из БД.

        Args:
        ----
            field (Literal["id", "name"]): название поля строкой на выбор.
            value (int | str): значение поля.

        Returns:
        -------
            Rack: сам экземляр полученной модели.

        """
        sql_command = f"""
            SELECT id, name
            FROM rack
            WHERE {field} = %s
        """  # noqa: S608
        with Rack.db() as conn:
            cur = conn.cursor()
            cur.execute(sql_command, (value,))
            data = cur.fetchone()
            return Rack(*data)

    def __str__(self: "Rack") -> str:
        """Строковое представление.

        Args:
        ----
            self (Rack): стеллаж.

        Returns:
        -------
            str: строковое представление.

        """
        return f"Стеллаж {self.name}"


class Order(BaseModel):
    """Класс, представлющий заказ."""

    db: Database = db

    def __init__(
        self: "Order",
        id_: int,
        order_number: int,
        consumer_name: str,
    ) -> None:
        """Конструктор.

        Args:
        ----
            self (Rack): сам экземпляр.
            id_ (int): id из базы.
            order_number (int): номер заказа.
            consumer_name (str): имя покупателя из базы.

        """
        self.id = id_
        self.order_number = order_number
        self.consumer_name = consumer_name

    @staticmethod
    def get_by(field: Literal["id", "order_number"], value: int) -> "Order":
        """Получить по названию поля и значению запись из БД.

        Args:
        ----
            field (Literal["id", "order_number"]): название
            поля строкой на выбор.
            value (int): значение поля.

        Returns:
        -------
            Rack: сам экземляр полученной модели.

        """
        sql_command = f"""
            SELECT id, order_number, consumer_name
            FROM ordert
            WHERE {field} = %s
        """  # noqa: S608
        with Order.db() as conn:
            cur = conn.cursor()
            cur.execute(sql_command, (value,))
            data = cur.fetchone()
            return Order(*data)

    def __str__(self: "Order") -> str:
        """Строковое представление.

        Args:
        ----
            self (Order): заказ.

        Returns:
        -------
            str: строковое представление.

        """
        return f"Заказ №{self.order_number}"


class Product(BaseModel):
    """Класс, представлющий товар."""

    db: Database = db

    def __init__(self: "Product", id_: int, name: str, article: int) -> None:
        """Конструктор.

        Args:
        ----
            self (Rack): сам экземпляр.
            id_ (int): id из базы.
            name (str): название товара.
            article (int): артикл товара в виде числа.

        """
        self.id = id_
        self.name = name
        self.article = article

    @staticmethod
    def get_by(field: Literal["id", "article"], value: int) -> "Order":
        """Получить по названию поля и значению запись из БД.

        Args:
        ----
            field (Literal["id", "order_number"]): название
            поля строкой на выбор.
            value (int): значение поля.

        Returns:
        -------
            Product: сам экземляр полученной модели.

        """
        sql_command = f"""
            SELECT id, name, article
            FROM product
            WHERE {field} = %s
        """  # noqa: S608
        with Product.db() as conn:
            cur = conn.cursor()
            cur.execute(sql_command, (value,))
            data = cur.fetchone()
            return Product(*data)

    def __str__(self: "Product") -> str:
        """Строковое представление.

        Args:
        ----
            self (Product): товар.

        Returns:
        -------
            str: строковое представление.

        """
        return f"Товар {self.name}"


class OrderProductLink(BaseModelLink):
    """Класс."""

    db: Database = db

    def __init__(
        self: "OrderProductLink",
        id_: int,
        order_id: int,
        product_id: int,
        count: int,
    ) -> None:
        """Конструктор.

        Args:
        ----
            self (Rack): сам экземпляр.
            id_ (int): id из базы.
            order_id (int): id соответвующего заказа.
            product_id (int): id соответвующего товара.
            count (int): количество соответствующих товаров в этом заказе.

        """
        self.id = id_
        self.order_id = order_id
        self.product_id = product_id
        self.count = count

    @staticmethod
    def get_all_by(
        field: Literal["order_id", "product_id"],
        value: int,
    ) -> list["OrderProductLink"]:
        """Получить по названию поля и значению запись из БД.

        Args:
        ----
            field (Literal["order_id", "product_id"]): название
            поля строкой на выбор.
            value (int): значение поля.

        Returns:
        -------
            list[OrderProductLink]: список экземляров полученной модели.

        """
        sql_command = f"""
            SELECT id, order_id, product_id, count
            FROM order_product_link
            WHERE {field} = %s
        """  # noqa: S608
        with OrderProductLink.db() as conn:
            cur = conn.cursor()
            cur.execute(sql_command, (value,))
            data = cur.fetchall()
            return [OrderProductLink(*row) for row in data]


class RackProductLink(BaseModelLink):
    """Класс."""

    db: Database = db

    def __init__(
        self: "RackProductLink",
        id_: int,
        rack_id: int,
        product_id: int,
        main: bool,  # noqa: FBT001
    ) -> None:
        """Конструктор.

        Args:
        ----
            self (Rack): сам экземпляр.
            id_ (int): id из базы.
            rack_id (int): id соответвующего стеллажа.
            product_id (int): id соответвующего товара.
            main (bool): является ли стеллаж главным для товара.

        """
        self.id = id_
        self.rack_id = rack_id
        self.product_id = product_id
        self.main = main

    @staticmethod
    def get_all_by(
        field: Literal["rack_id", "product_id"],
        value: int,
    ) -> list["RackProductLink"]:
        """Получить по названию поля и значению запись из БД.

        Args:
        ----
            field (Literal["rack_id", "product_id"]): название
            поля строкой на выбор.
            value (int): значение поля.

        Returns:
        -------
            list[RackProductLink]: список экземляров полученной модели.

        """
        sql_command = f"""
            SELECT id, rack_id, product_id, main
            FROM rack_product_link
            WHERE {field} = %s
        """  # noqa: S608
        with RackProductLink.db() as conn:
            cur = conn.cursor()
            cur.execute(sql_command, (value,))
            data = cur.fetchall()
            return [RackProductLink(*row) for row in data]
