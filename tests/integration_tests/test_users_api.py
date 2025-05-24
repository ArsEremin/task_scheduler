import pytest


class TestUsersAPI:
    @property
    def get_url(self):
        return "/users"

    @pytest.mark.parametrize(
        "login, password, status_code",
        [
            ("alex", "123", 200),
            ("petr", "1234", 200),
            ("ivan", "12345", 200),
            ("invalid_user", "100", 401),
        ]
    )
    async def test_login_user(self, async_client, login, password, status_code):
        response = await async_client.post(
            url=f"{self.get_url}/login",
            json={
                "login": login,
                "password": password
            }
        )

        assert response.status_code == status_code

        if status_code == 200:
            token = response.cookies.get("scheduler_access_token")
            assert token is not None

    async def test_auth_user_flow(self, async_client):
        login_response = await async_client.post(
            url=f"{self.get_url}/login",
            json={
                "login": "alex",
                "password": "123"
            }
        )

        assert login_response.status_code == 200
        token = login_response.cookies.get("scheduler_access_token")
        assert token is not None

        logout_response = await async_client.post(url=f"{self.get_url}/logout")

        assert logout_response.status_code == 200
        token = logout_response.cookies.get("scheduler_access_token")
        assert token is None
