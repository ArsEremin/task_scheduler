from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.users.service import UserService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.HASH_ALG0
    )
    return encoded_jwt


async def auth_user(session: AsyncSession, email: EmailStr, password: str):
    user = await UserService.get_by_filter(session, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
