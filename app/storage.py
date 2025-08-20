from __future__ import annotations

from threading import RLock
from typing import Dict, Iterable, Optional
from uuid import UUID

from .models import Task, TaskUpdate


class InMemoryTaskRepository:
    """Thread-safe in-memory repository for tasks."""

    def __init__(self) -> None:
        self._tasks: Dict[UUID, Task] = {}
        self._lock = RLock()

    def create(self, task: Task) -> Task:
        with self._lock:
            self._tasks[task.id] = task
            return task

    def get(self, task_id: UUID) -> Optional[Task]:
        with self._lock:
            return self._tasks.get(task_id)

    def list(self) -> Iterable[Task]:
        with self._lock:
            return list(self._tasks.values())

    def update(self, task_id: UUID, update: TaskUpdate) -> Optional[Task]:
        with self._lock:
            existing = self._tasks.get(task_id)
            if existing is None:
                return None
            if update.title is not None:
                existing.title = update.title
            if update.description is not None:
                existing.description = update.description
            if update.status is not None:
                existing.status = update.status
            self._tasks[task_id] = existing
            return existing

    def delete(self, task_id: UUID) -> bool:
        with self._lock:
            return self._tasks.pop(task_id, None) is not None

    def clear(self) -> None:
        with self._lock:
            self._tasks.clear()


# Singleton repository instance for app usage
repository = InMemoryTaskRepository()


