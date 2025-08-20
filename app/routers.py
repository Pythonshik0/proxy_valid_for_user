from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response, status
from typing import List
from uuid import UUID

from .models import Task, TaskCreate, TaskUpdate
from .storage import repository


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> Task:
    task = Task(title=payload.title, description=payload.description)
    return repository.create(task)


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: UUID) -> Task:
    task = repository.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.get("", response_model=List[Task])
def list_tasks() -> List[Task]:
    return list(repository.list())


@router.put("/{task_id}", response_model=Task)
def update_task(task_id: UUID, payload: TaskUpdate) -> Task:
    updated = repository.update(task_id, payload)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return updated


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID) -> Response:
    deleted = repository.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


