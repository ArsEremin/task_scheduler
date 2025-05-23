from typing import Annotated

from fastapi import APIRouter, Depends, status, Response

from src.users.dependencies import get_current_user
from src.users.models import User
from src.users.utils import create_access_token
from src.users.schemas import UserAuthSchema
from src.users.service import UserService, get_user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    response: Response,
    service: Annotated[UserService, Depends(get_user_service)],
    user_auth_data: UserAuthSchema
):
    user = await service.auth_user(user_auth_data.login, user_auth_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("scheduler_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("scheduler_access_token")
    return {"status": "ok"}


@router.get("/me")
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
