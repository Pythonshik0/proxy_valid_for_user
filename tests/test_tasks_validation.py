from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_task_validation_error_on_empty_title() -> None:
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422


def test_update_task_invalid_status() -> None:
    created = client.post("/tasks", json={"title": "x"}).json()
    task_id = created["id"]
    response = client.put(f"/tasks/{task_id}", json={"status": "unknown"})
    assert response.status_code == 422


