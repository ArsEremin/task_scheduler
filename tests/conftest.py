import asyncio
import json
from datetime import datetime

import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient, ASGITransport

from src.main import app as fastapi_app
from src.config import settings
from src.database import engine, Base, async_session_maker
from src.tasks.models import Task
from src.tasks.service import TaskService
from src.users.models import User
from src.users.service import UserService
from src.users.utils import get_password_hash


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
async def user_service(session: AsyncSession):
    return UserService(session)


@pytest.fixture(scope="session")
async def task_service(session: AsyncSession):
    return TaskService(session)


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    assert settings.MODE == "TEST"

    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        table_names = (("users", User), ("tasks", Task))
        for json_name, table_name in table_names:
            with open(f"tests/test_data/{json_name}.json", 'r', encoding="utf-8") as file:
                values = json.load(file)

            if json_name == "users":
                for user in values:
                    user["hashed_password"] = get_password_hash(user["hashed_password"])

            if json_name == "tasks":
                for val in values:
                    val["due_date"] = datetime.strptime(val["due_date"], "%Y-%m-%d")

            await conn.execute(insert(table_name), values)
            await conn.commit()


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def auth_client():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        await ac.post(
            url="users/login",
            json={
                "login": "alex",
                "password": "123"
            }
        )
        assert ac.cookies["scheduler_access_token"]
        yield ac
