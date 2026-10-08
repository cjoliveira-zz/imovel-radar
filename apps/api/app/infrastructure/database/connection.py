from __future__ import annotations

import os
from collections.abc import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


class DatabaseSettings:
    def __init__(self, database_url: str | None = None) -> None:
        self.database_url = database_url or os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://imovelradar:imovelradar@localhost:5432/imovelradar",
        )

    def get_engine(self) -> Engine:
        return create_engine(self.database_url, pool_pre_ping=True, future=True)


def get_engine() -> Engine:
    settings = DatabaseSettings()
    return settings.get_engine()


SessionLocal = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False, future=True)


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
