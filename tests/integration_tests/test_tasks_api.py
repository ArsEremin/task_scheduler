class TestTasksAPI:
    @property
    def get_url(self):
        return "/tasks"

    async def test_get_task(self, auth_client):
        response_200 = await auth_client.get(url=f"{self.get_url}/1")
        response_404 = await auth_client.get(url=f"{self.get_url}/10")

        assert response_200.status_code == 200
        assert response_404.status_code == 404

    async def test_create_task(self, auth_client):
        valid_task_data = {
            "title": "new task",
            "description": "new task for ivan",
            "created_by": 1,
            "status": "todo",
            "priority": "low",
            "assignee": "ivan",
            "due_date": "2025-09-05"
        }

        invalid_task_data = valid_task_data.copy()
        invalid_task_data["assignee"] = "invalid user"

        response_201 = await auth_client.post(
            url=f"{self.get_url}",
            json=valid_task_data
        )

        assert response_201.status_code == 201

        response_404 = await auth_client.post(
            url=f"{self.get_url}",
            json=invalid_task_data
        )

        assert response_404.status_code == 404
