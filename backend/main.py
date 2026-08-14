import os
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DB_PATH = os.getenv("DB_PATH", "./minitask.db")
DEMO_TOKEN = "minitask-demo-token"

app = FastAPI(title="MiniTask API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def now():
    return datetime.now(timezone.utc).isoformat()


def conn():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    parent = os.path.dirname(DB_PATH)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with closing(conn()) as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                title TEXT,
                description TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'todo',
                priority TEXT NOT NULL DEFAULT 'medium',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )
        count = db.execute("SELECT COUNT(*) AS c FROM projects").fetchone()["c"]
        if count == 0:
            cur = db.execute(
                "INSERT INTO projects(name, description, created_at) VALUES(?,?,?)",
                ("SmartHub Demo", "用于 SmartHub 自动化测试的示例项目", now()),
            )
            pid = cur.lastrowid
            seed = [
                (pid, "完成登录页", "", "completed", "high"),
                (pid, "补充 API 文档", "", "in_progress", "medium"),
                (pid, "执行回归测试", "", "todo", "high"),
            ]
            for project_id, title, desc, status, priority in seed:
                t = now()
                db.execute(
                    "INSERT INTO tasks(project_id,title,description,status,priority,created_at,updated_at) VALUES(?,?,?,?,?,?,?)",
                    (project_id, title, desc, status, priority, t, t),
                )
        db.commit()


@app.on_event("startup")
def startup():
    init_db()


class LoginBody(BaseModel):
    username: str
    password: str


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = ""


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = None


class TaskCreate(BaseModel):
    project_id: int
    title: str = ""  # BUG-02: 需求要求标题不能为空，这里故意允许空字符串
    description: str = ""
    status: str = "todo"
    priority: str = "medium"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None


class StatusBody(BaseModel):
    status: str


def require_auth(authorization: Optional[str] = Header(default=None)):
    if authorization != f"Bearer {DEMO_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")


def row_dict(row):
    return dict(row) if row else None


def ensure_choice(value: str, allowed: set[str], field: str):
    if value not in allowed:
        raise HTTPException(status_code=400, detail=f"invalid {field}")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "minitask"}


@app.post("/api/login")
def login(body: LoginBody):
    # BUG-01: admin 用户即使密码错误也会拿到 200 + token。
    if body.username == "admin":
        return {"token": DEMO_TOKEN, "username": "admin"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/api/projects", dependencies=[Depends(require_auth)])
def list_projects():
    with closing(conn()) as db:
        rows = db.execute("SELECT * FROM projects ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]


@app.post("/api/projects", dependencies=[Depends(require_auth)], status_code=201)
def create_project(body: ProjectCreate):
    with closing(conn()) as db:
        cur = db.execute(
            "INSERT INTO projects(name,description,created_at) VALUES(?,?,?)",
            (body.name.strip(), body.description, now()),
        )
        db.commit()
        return row_dict(db.execute("SELECT * FROM projects WHERE id=?", (cur.lastrowid,)).fetchone())


@app.put("/api/projects/{project_id}", dependencies=[Depends(require_auth)])
def update_project(project_id: int, body: ProjectUpdate):
    with closing(conn()) as db:
        current = db.execute("SELECT * FROM projects WHERE id=?", (project_id,)).fetchone()
        if not current:
            raise HTTPException(status_code=404, detail="Project not found")
        name = body.name.strip() if body.name is not None else current["name"]
        description = body.description if body.description is not None else current["description"]
        db.execute("UPDATE projects SET name=?, description=? WHERE id=?", (name, description, project_id))
        db.commit()
        return row_dict(db.execute("SELECT * FROM projects WHERE id=?", (project_id,)).fetchone())


@app.delete("/api/projects/{project_id}", dependencies=[Depends(require_auth)])
def delete_project(project_id: int):
    with closing(conn()) as db:
        exists = db.execute("SELECT id FROM projects WHERE id=?", (project_id,)).fetchone()
        if not exists:
            raise HTTPException(status_code=404, detail="Project not found")
        # BUG-03: 故意不级联删除 tasks，形成孤儿任务。
        db.execute("DELETE FROM projects WHERE id=?", (project_id,))
        db.commit()
        return {"deleted": True, "id": project_id}


@app.get("/api/tasks", dependencies=[Depends(require_auth)])
def list_tasks(
    project_id: Optional[int] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    keyword: Optional[str] = Query(default=None, max_length=100),
):
    sql = "SELECT * FROM tasks WHERE 1=1"
    args = []
    if project_id is not None:
        sql += " AND project_id=?"
        args.append(project_id)
    if status:
        sql += " AND status=?"
        args.append(status)
    if priority:
        # BUG-05: high 筛选错误地使用 medium。
        sql += " AND priority=?"
        args.append("medium" if priority == "high" else priority)
    if keyword:
        sql += " AND (title LIKE ? OR description LIKE ?)"
        args.extend([f"%{keyword}%", f"%{keyword}%"])
    sql += " ORDER BY id DESC"
    with closing(conn()) as db:
        return [dict(r) for r in db.execute(sql, args).fetchall()]


@app.post("/api/tasks", dependencies=[Depends(require_auth)], status_code=201)
def create_task(body: TaskCreate):
    ensure_choice(body.status, {"todo", "in_progress", "completed"}, "status")
    ensure_choice(body.priority, {"high", "medium", "low"}, "priority")
    with closing(conn()) as db:
        project = db.execute("SELECT id FROM projects WHERE id=?", (body.project_id,)).fetchone()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        t = now()
        cur = db.execute(
            "INSERT INTO tasks(project_id,title,description,status,priority,created_at,updated_at) VALUES(?,?,?,?,?,?,?)",
            (body.project_id, body.title, body.description, body.status, body.priority, t, t),
        )
        db.commit()
        return row_dict(db.execute("SELECT * FROM tasks WHERE id=?", (cur.lastrowid,)).fetchone())


@app.get("/api/tasks/{task_id}", dependencies=[Depends(require_auth)])
def get_task(task_id: int):
    with closing(conn()) as db:
        task = db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return dict(task)


@app.put("/api/tasks/{task_id}", dependencies=[Depends(require_auth)])
def update_task(task_id: int, body: TaskUpdate):
    with closing(conn()) as db:
        current = db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if not current:
            raise HTTPException(status_code=404, detail="Task not found")
        title = current["title"] if body.title is None else body.title
        description = current["description"] if body.description is None else body.description
        status = current["status"] if body.status is None else body.status
        priority = current["priority"] if body.priority is None else body.priority
        ensure_choice(status, {"todo", "in_progress", "completed"}, "status")
        ensure_choice(priority, {"high", "medium", "low"}, "priority")
        db.execute(
            "UPDATE tasks SET title=?,description=?,status=?,priority=?,updated_at=? WHERE id=?",
            (title, description, status, priority, now(), task_id),
        )
        db.commit()
        return row_dict(db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone())


@app.patch("/api/tasks/{task_id}/status", dependencies=[Depends(require_auth)])
def change_status(task_id: int, body: StatusBody):
    ensure_choice(body.status, {"todo", "in_progress", "completed"}, "status")
    with closing(conn()) as db:
        current = db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if not current:
            raise HTTPException(status_code=404, detail="Task not found")
        # BUG-04: 未验证 todo -> in_progress -> completed 的单向状态机，可回退。
        db.execute("UPDATE tasks SET status=?,updated_at=? WHERE id=?", (body.status, now(), task_id))
        db.commit()
        return row_dict(db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone())


@app.delete("/api/tasks/{task_id}", dependencies=[Depends(require_auth)])
def delete_task(task_id: int):
    with closing(conn()) as db:
        cur = db.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        db.commit()
        return {"deleted": True, "id": task_id}


@app.get("/api/dashboard", dependencies=[Depends(require_auth)])
def dashboard():
    with closing(conn()) as db:
        projects = db.execute("SELECT COUNT(*) AS c FROM projects").fetchone()["c"]
        tasks = db.execute("SELECT COUNT(*) AS c FROM tasks").fetchone()["c"]
        completed = db.execute("SELECT COUNT(*) AS c FROM tasks WHERE status='completed'").fetchone()["c"]
        # BUG-06: 已完成数故意 +1，未完成数因此也会偏差。
        wrong_completed = completed + 1
        return {
            "projects": projects,
            "tasks": tasks,
            "completed": wrong_completed,
            "unfinished": max(tasks - wrong_completed, 0),
        }
