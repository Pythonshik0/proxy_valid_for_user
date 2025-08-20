from __future__ import annotations

from fastapi import FastAPI

from .routers import router as tasks_router


def create_app() -> FastAPI:
    app = FastAPI(title="Task Manager", version="1.0.0")
    app.include_router(tasks_router)
    return app


app = create_app()


