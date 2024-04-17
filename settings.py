"""Модуль настроек для работы приложения."""

from pathlib import Path

from envparse import env

from database import Database, DatabaseSettings

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.is_file():
    env.read_envfile(ENV_PATH)

settings = DatabaseSettings(
    host=env.str("POSTGRES_HOST"),
    port=env.int("POSTGRES_PORT"),
    db=env.str("POSTGRES_DB"),
    user=env.str("POSTGRES_USER"),
    password=env.str("POSTGRES_PASSWORD"),
)

db = Database(settings=settings)
