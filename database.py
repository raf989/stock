"""Модуль классов для работы базы данных."""

from typing import NamedTuple

import psycopg2


class DatabaseSettings(NamedTuple):
    """Именнованный кортеж.

    Хранит необходимые настройки для подключения БД.
    """

    host: str
    port: int
    db: str
    user: str
    password: str


class Database:
    """Объект для создание подключения к базе данных."""

    def __init__(self: "Database", *, settings: DatabaseSettings) -> None:
        """Конструктор класса.

        Args:
        ----
            self (Database): сам объект.
            settings (DatabaseSettings): кортеж настроек для подключения.

        """
        self.__settings = settings

    def __call__(self: "Database") -> "Database.Connection":
        """Создание подключения."""
        return Database.Connection(self.__settings)

    class Connection:
        """Подключение к базе (замкнутые настройки подключения)."""

        def __init__(
            self: "Database.Connection",
            settings: DatabaseSettings,
        ) -> None:
            """Конструктор подключения.

            Args:
            ----
                self (Database.Connection): само подключение.
                settings (DatabaseSettings): настройки подключения.

            """
            self.__settings = settings

        def __enter__(self: "Database.Connection") -> object:
            """Создание подключения."""
            self._connection = psycopg2.connect(
                host=self.__settings.host,
                port=self.__settings.port,
                dbname=self.__settings.db,
                user=self.__settings.user,
                password=self.__settings.password,
            )
            return self._connection

        def __exit__(self: "Database.Connection", *args: object) -> None:
            """Закрытие подключения."""
            self._connection.close()
