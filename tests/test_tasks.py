from __future__ import annotations

from typing import Any, Dict
from uuid import UUID

from fastapi.testclient import TestClient

from app.main import app
from app.storage import repository
from app.models import TaskStatus


client = TestClient(app)


def setup_function(_: Any) -> None:
    repository.clear()


def test_create_task() -> None:
    payload: Dict[str, Any] = {"title": "Task A", "description": "Desc"}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert UUID(data["id"])  # valid UUID
    assert data["title"] == "Task A"
    assert data["description"] == "Desc"
    assert data["status"] == TaskStatus.created.value


def test_get_task() -> None:
    created = client.post("/tasks", json={"title": "T"}).json()
    task_id = created["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_get_task_not_found() -> None:
    response = client.get("/tasks/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_list_tasks() -> None:
    client.post("/tasks", json={"title": "A"})
    client.post("/tasks", json={"title": "B"})
    response = client.get("/tasks")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) == 2


def test_update_task_title_and_status() -> None:
    created = client.post("/tasks", json={"title": "Old"}).json()
    task_id = created["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "New", "status": TaskStatus.in_progress.value},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New"
    assert data["status"] == TaskStatus.in_progress.value


def test_delete_task() -> None:
    created = client.post("/tasks", json={"title": "To delete"}).json()
    task_id = created["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    get_after = client.get(f"/tasks/{task_id}")
    assert get_after.status_code == 404


