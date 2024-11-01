from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import delete, insert
from sqlalchemy.exc import (
    DBAPIError,
    IntegrityError,
    MultipleResultsFound,
    NoResultFound,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import load_only

from core.exceptions import (
    AlreadyExistError,
    DBError,
    MultipleRowsFoundError,
    NoRowsFoundError,
)


class AbstractRepository(ABC):
    model = None

    @abstractmethod
    async def all(self, **filters):
        raise NotImplementedError

    @abstractmethod
    async def filter(self, **filters):
        raise NotImplementedError

    @abstractmethod
    async def create(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, pk: Optional[int], **kwargs):
        raise NotImplementedError


class BaseRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict):
        stmt = insert(self.model).values(data).returning(self.model)

        try:
            result = await self.session.execute(stmt)
        except IntegrityError:
            raise AlreadyExistError(
                f"object {self.model.__name__} already exist or no related tables with it"
            )
        return result.scalar()

    async def bulk_create(self, data: list[dict]):
        stmt = insert(self.model).values(data).returning(self.model)
        try:
            result = await self.session.execute(stmt)
        except IntegrityError:
            raise AlreadyExistError(
                f"object {self.model.__name__} already exist or no related tables with it"
            )
        return result.scalar()

    async def update(self, data: dict, filters=None):
        if not data:
            raise DBError(
                f"Passed empty dictionary for update method in model {self.model.__name__}"
            )

        query = select(self.model)
        if filters:
            query = query.filter_by(**filters)
        try:
            result = await self.session.execute(query)
            obj = result.one()[0]
        except NoResultFound:
            raise NoRowsFoundError(f"For model {self.model.__name__} with filters: {filters}")
        except DBAPIError as e:
            raise DBError(str(e))

        for key, value in data.items():
            if not hasattr(obj, key):
                raise DBError(f"Field {key} not exists in {self.model.__name__}")
            setattr(obj, key, value)

        try:
            await self.session.commit()
        except IntegrityError:
            raise AlreadyExistError(
                f"object {self.model.__name__} already exist or no related tables with it"
            )
        return obj

    async def delete(self, **filters):
        result = await self.session.execute(delete(self.model).filter_by(**filters))
        if result.rowcount == 0:
            raise NoRowsFoundError(f"For model {self.model.__name__} with next filters:{filters}")

    async def filter(
        self,
        filters: dict | None = None,
        fields: list[str] | None = None,
        order: dict | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ):
        stmt = select(self.model)
        if filters:
            stmt = stmt.filter_by(**filters)
        if fields:
            model_fields = [getattr(self.model, field) for field in fields]
            stmt = stmt.options(load_only(*model_fields))
        if order is not None:
            stmt = stmt.order_by(order)
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)

        row = await self.session.execute(stmt)
        return row.scalars().all()

    async def get_one(self, **filters):
        row = await self.session.execute(select(self.model).filter_by(**filters))
        try:
            result = row.scalar_one()
        except NoResultFound:
            raise NoRowsFoundError(f"For model {self.model.__name__} with next filters:{filters}")
        except MultipleResultsFound:
            raise MultipleRowsFoundError(
                f"For model {self.model.__name__} with next filters:{filters}"
            )
        return result

    async def exists(self, **filters) -> bool:
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalar() is not None

    async def all(self):
        return await self.filter()
