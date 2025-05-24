from datetime import datetime

import pytest


class TestTaskService:
    @pytest.mark.parametrize(
        "task_id, title, description, status, assignee_id, is_exist",
        [
            (1, "task1", "task for alex", "todo", 1, True),
            (2, "task2", "task for petr", "in_progress", 2, True),
            (3, "task3", "task for ivan", "done", 3, True),
            (100, "invalid task", "invalid", "INVALID", 5, False),
        ]

    )
    async def test_get_task_by_id(
        self, task_service, task_id, title,
        description, status, assignee_id, is_exist
    ):
        task = await task_service.get_task_by_id(task_id)

        if is_exist:
            assert task.id == task_id and task.title == title and task.description == description\
                   and task.status == status and task.assignee_id == assignee_id
        else:
            assert task is None

    @pytest.mark.parametrize(
        "filters",
        [
            {"status": "todo", "priority": "low", "assignee_id": 1},
            {"status": "in_progress"},
            {"priority": "high"},
            {"assignee_id": 2},
            {"status": "done", "assignee_id": 3}
        ]
    )
    async def test_get_tasks_by_filters(self, task_service, filters):
        tasks = await task_service.get_tasks_by_filters(**filters)
        assert len(tasks) == 1

    async def test_add_task(self, task_service):
        task_data = {
            "title": "new task",
            "description": "new task for ivan",
            "created_by": 1,
            "status": "todo",
            "priority": "low",
            "assignee_id": 3,
            "due_date": datetime.strptime("2025-09-05", "%Y-%m-%d")
        }
        new_task = await task_service.add_task(task_data)

        assert new_task is not None
        assert new_task.title == task_data["title"] and new_task.description == task_data["description"]
        assert new_task.assignee_id == task_data["assignee_id"]
