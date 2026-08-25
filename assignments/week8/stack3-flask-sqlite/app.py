from pathlib import Path
import sqlite3

from flask import Flask, g, jsonify, render_template, request

app = Flask(__name__)
app.config["DATABASE"] = Path(__file__).with_name("tasks.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        get_db().execute(
            """CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                notes TEXT NOT NULL DEFAULT '',
                completed INTEGER NOT NULL DEFAULT 0 CHECK(completed IN (0, 1)),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        get_db().commit()


def task_dict(row):
    result = dict(row)
    result["completed"] = bool(result["completed"])
    return result


def find_task(task_id):
    row = get_db().execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return row


def validate(data):
    if not isinstance(data, dict):
        return None, "请求体必须是 JSON 对象"
    title = str(data.get("title", "")).strip()
    notes = str(data.get("notes", "")).strip()
    if not title:
        return None, "标题不能为空"
    if len(title) > 120:
        return None, "标题最多 120 字"
    if len(notes) > 2000:
        return None, "备注最多 2000 字"
    return {"title": title, "notes": notes, "completed": bool(data.get("completed", False))}, None


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/tasks")
def list_tasks():
    rows = get_db().execute("SELECT * FROM tasks ORDER BY created_at DESC, id DESC").fetchall()
    return jsonify([task_dict(row) for row in rows])


@app.get("/api/tasks/<int:task_id>")
def read_task(task_id):
    row = find_task(task_id)
    if row is None:
        return jsonify(error="任务不存在"), 404
    return jsonify(task_dict(row))


@app.post("/api/tasks")
def create_task():
    data, error = validate(request.get_json(silent=True))
    if error:
        return jsonify(error=error), 422
    db = get_db()
    cursor = db.execute(
        "INSERT INTO tasks (title, notes, completed) VALUES (?, ?, ?)",
        (data["title"], data["notes"], int(data["completed"])),
    )
    db.commit()
    return jsonify(task_dict(find_task(cursor.lastrowid))), 201


@app.put("/api/tasks/<int:task_id>")
def update_task(task_id):
    if find_task(task_id) is None:
        return jsonify(error="任务不存在"), 404
    data, error = validate(request.get_json(silent=True))
    if error:
        return jsonify(error=error), 422
    db = get_db()
    db.execute(
        """UPDATE tasks SET title = ?, notes = ?, completed = ?,
           updated_at = CURRENT_TIMESTAMP WHERE id = ?""",
        (data["title"], data["notes"], int(data["completed"]), task_id),
    )
    db.commit()
    return jsonify(task_dict(find_task(task_id)))


@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    db = get_db()
    cursor = db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    if cursor.rowcount == 0:
        return jsonify(error="任务不存在"), 404
    return "", 204


init_db()

if __name__ == "__main__":
    app.run(debug=True)
