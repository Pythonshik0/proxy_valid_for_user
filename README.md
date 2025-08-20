## Task Manager (FastAPI + pytest)

FastAPI CRUD сервис для управления задачами с UUID и статусами: `created`, `in_progress`, `completed`.

### Запуск локально

```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger UI: `http://127.0.0.1:8000/docs`

### Тесты

```bash
pytest
```

### API
- POST `/tasks` — создание задачи
- GET `/tasks/{id}` — получение задачи
- GET `/tasks` — список задач
- PUT `/tasks/{id}` — обновление задачи (title, description, status)
- DELETE `/tasks/{id}` — удаление задачи

### Примечания
- Хранилище в памяти, очищается между тестами и перезапусками.
- Валидация через Pydantic. Статусы: `created`, `in_progress`, `completed`.


<<<<<<< HEAD
=======
---

**Контакты для связи:**
- 89870545519
>>>>>>> origin/main
