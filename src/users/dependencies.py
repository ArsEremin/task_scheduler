from datetime import datetime, timezone
from typing import Annotated

import jwt
from fastapi import Cookie, Depends, HTTPException, status

from src.config import settings
from src.users.exceptions import InvalidTokenException, TokenExpiredException
from src.users.service import UserService, get_user_service


def get_token(scheduler_access_token: Annotated[str | None, Cookie()] = None):
    if not scheduler_access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return scheduler_access_token


async def get_current_user(
    service: Annotated[UserService, Depends(get_user_service)],
    token: Annotated[str, Depends(get_token)]
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.HASH_ALG0
        )
    except jwt.exceptions.PyJWTError:
        raise InvalidTokenException
    expire: str = payload.get("exp")
    user_id: str = payload.get("sub")
    if not expire or not user_id:
        raise InvalidTokenException
    if int(expire) < datetime.now(timezone.utc).timestamp():
        raise TokenExpiredException
    user = await service.get_user_by_id(int(user_id))
    if not user:
        raise InvalidTokenException
    return user
