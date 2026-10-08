from __future__ import annotations

from collections.abc import Iterable
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.database.models import ListingModel, PropertyModel, SourceModel

T = TypeVar("T")


class RepositoryBase:
    model: type[T]

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, instance: T) -> T:
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def get_by_id(self, instance_id: object) -> T | None:
        return self.session.get(self.model, instance_id)

    def list_all(self) -> list[T]:
        return list(self.session.scalars(select(self.model)).all())


class SourceRepository(RepositoryBase):
    model = SourceModel


class PropertyRepository(RepositoryBase):
    model = PropertyModel


class ListingRepository(RepositoryBase):
    model = ListingModel
