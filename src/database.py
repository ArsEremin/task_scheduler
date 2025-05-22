from datetime import datetime, timezone
from typing import AsyncGenerator, Annotated

from sqlalchemy import TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column

from src.config import settings

engine = create_async_engine(settings.get_database_uri)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    intpk = Annotated[int, mapped_column(primary_key=True)]
    utc_datetime = Annotated[datetime, mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))]

    def __repr__(self):
        cols = [f"{col}={getattr(self, col)}" for col in self.__table__.columns.keys()]
        return f"{self.__class__.__name__}({','.join(cols)})"
