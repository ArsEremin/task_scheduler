import pytest


class TestUserService:
    @pytest.mark.parametrize(
        "user_id, username, email, is_exist",
        [
            (1, "alex", "alex@test.com", True),
            (2, "petr", "petr@test.com", True),
            (3, "ivan", "ivan@test.com", True),
            (333, "invalid", "invalid@invalid.com", False)
        ]
    )
    async def test_get_user_by_id(self, user_service, user_id, username, email, is_exist):
        user = await user_service.get_user_by_id(user_id)
        if is_exist:
            assert user.id == user_id and user.username == username and user.email == email
        else:
            assert user is None

    @pytest.mark.parametrize(
        "user_id, username, email, is_exist",
        [
            (1, "alex", "alex@test.com", True),
            (2, "petr", "petr@test.com", True),
            (3, "ivan", "ivan@test.com", True),
            (333, "invalid", "invalid@invalid.com", False)
        ]
    )
    async def test_get_user_by_login(self, user_service, user_id, username, email, is_exist):
        user_by_username = await user_service.get_user_by_login(username)
        user_by_email = await user_service.get_user_by_login(email)

        if is_exist:
            assert user_by_username.username == username
            assert user_by_email.email == email
            assert user_by_username == user_by_email
            assert user_by_username.id == user_id and user_by_username.email == email
        else:
            assert user_by_username is None
            assert user_by_email is None
