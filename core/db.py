"""模块 0 · 本地存储（SQLite）

表结构故意做浅：一门课一条记录，结构化数据整体存 JSON 字符串。

理由（写进技术文档第 3 章）：
27 天内不值得为关系建模花时间；而且「删掉 data/app.db 就能干净重跑」
对评审复现是极其友好的特性 —— 复现成本越低，越容易拿到可复现性的分。
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

DB_PATH = Path("data/app.db")


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """建表。幂等，可重复调用。"""
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS courses (
                course_id   TEXT PRIMARY KEY,
                name        TEXT NOT NULL,
                payload     TEXT NOT NULL,
                updated_at  TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
            )
            """
        )


def save_course(course_id: str, name: str, payload: dict) -> None:
    """保存或覆盖一门课的全部数据。"""
    init_db()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO courses (course_id, name, payload, updated_at)
            VALUES (?, ?, ?, datetime('now', 'localtime'))
            ON CONFLICT(course_id) DO UPDATE SET
                name = excluded.name,
                payload = excluded.payload,
                updated_at = excluded.updated_at
            """,
            (course_id, name, json.dumps(payload, ensure_ascii=False)),
        )


def load_course(course_id: str) -> dict | None:
    """读取一门课；不存在返回 None。"""
    init_db()
    with _connect() as conn:
        row = conn.execute(
            "SELECT payload FROM courses WHERE course_id = ?", (course_id,)
        ).fetchone()
    if row is None:
        return None
    return json.loads(row["payload"])


def list_courses() -> list[dict]:
    """列出全部课程，按更新时间倒序。"""
    init_db()
    with _connect() as conn:
        rows = conn.execute(
            "SELECT course_id, name, updated_at FROM courses ORDER BY updated_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def delete_course(course_id: str) -> None:
    init_db()
    with _connect() as conn:
        conn.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
