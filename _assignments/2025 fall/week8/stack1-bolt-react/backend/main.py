from contextlib import asynccontextmanager
from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DB_PATH = Path(__file__).with_name("tasks.db")


def connection() -> sqlite3.Connection:
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def init_db() -> None:
    with connection() as db:
        db.execute(
            """CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                notes TEXT NOT NULL DEFAULT '',
                completed INTEGER NOT NULL DEFAULT 0 CHECK(completed IN (0, 1)),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )"""
        )


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Focus Notes API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskInput(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    notes: str = Field(default="", max_length=2000)
    completed: bool = False


class Task(TaskInput):
    id: int
    created_at: str
    updated_at: str


def clean(payload: TaskInput) -> TaskInput:
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=422, detail="Title cannot be blank")
    return TaskInput(title=title, notes=payload.notes.strip(), completed=payload.completed)


def get_task(task_id: int) -> dict:
    with connection() as db:
        row = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    result = dict(row)
    result["completed"] = bool(result["completed"])
    return result


@app.get("/api/tasks", response_model=list[Task])
def list_tasks():
    with connection() as db:
        rows = db.execute("SELECT * FROM tasks ORDER BY created_at DESC, id DESC").fetchall()
    return [{**dict(row), "completed": bool(row["completed"])} for row in rows]


@app.get("/api/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    return get_task(task_id)


@app.post("/api/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskInput):
    item = clean(payload)
    with connection() as db:
        cursor = db.execute(
            "INSERT INTO tasks (title, notes, completed) VALUES (?, ?, ?)",
            (item.title, item.notes, int(item.completed)),
        )
        task_id = cursor.lastrowid
    return get_task(task_id)


@app.put("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskInput):
    get_task(task_id)
    item = clean(payload)
    with connection() as db:
        db.execute(
            """UPDATE tasks SET title = ?, notes = ?, completed = ?,
               updated_at = CURRENT_TIMESTAMP WHERE id = ?""",
            (item.title, item.notes, int(item.completed), task_id),
        )
    return get_task(task_id)


@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    with connection() as db:
        cursor = db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
