from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.users.utils import verify_password, get_password_hash
from src.users.exceptions import InvalidAuthDataException
from src.users.models import User


class UserService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_by_id(self, user_id: int):
        query = select(User).filter_by(id=user_id)
        res = await self._session.execute(query)
        return res.scalar_one_or_none()

    async def get_user_by_login(self, login: str):
        query = select(User).where(or_(User.email == login, User.username == login))
        res = await self._session.execute(query)
        return res.scalar_one_or_none()

    async def auth_user(self, login: str, password: str):
        user = await self.get_user_by_login(login)
        if user is None or not verify_password(password, user.hashed_password):
            raise InvalidAuthDataException
        return user

    async def insert_user(self):
        data = {"username": "sasha", "email": "sasha@gmail.com", "hashed_password": get_password_hash("123")}
        user = User(**data)
        self._session.add(user)
        await self._session.commit()


async def get_user_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> UserService:
    return UserService(session)
