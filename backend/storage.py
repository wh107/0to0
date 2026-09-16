# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 11:33:34 2026

@author: Administrator
"""

# import json  # 标准库|更换1
import sqlite3

# 定义用于存储内容的json文件
# HISTORY_FILE = "history.json" #更换2
DB_FILE = "history.db"


# 连接库
def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # 让查询结果带上列名（默认是元组）
    return conn


# 建表|更改3
def init_db():
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                text TEXT,
                score REAL,
                label TEXT,
                pinyin TEXT,
                created_at TEXT
            )
        """)
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_history_session_created "
            "ON history(session_id, created_at)"
        )
        conn.commit()  # 提交建表操作（无论是否新建，都确保事务结束）
    except Exception as e:
        print("建表失败：", e)
    finally:
        conn.close()  # 确保连接关闭


# 读文件
# def load_history(): #更换6
#     try:
#         with open(HISTORY_FILE, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return []
# 原本用于将数据从json文件读到内存里面，但之后没有认回去调用。直接从数据库里取了，
# 所以直接删除掉即可。


# 先读出文件，再添加，最后写数据到文件
# def save_record(record): #更换4
#     records = load_history()
#     records.append(record)
#     with open(HISTORY_FILE, "w", encoding="utf-8") as f:
#         json.dump(records, f, ensure_ascii=False, indent=2)
# def save_record(record):
#     values = [
#         record["text"],
#         record["score"],
#         record["label"],
#         record["pinyin"],
#         record["created_at"],
#     ]

#     conn = get_conn()
#     try:
#         cur = conn.cursor()
#         cur.execute(
#             """
#             INSERT INTO history 
#             (text, score, label, pinyin, created_at)
#             VALUES (?, ?, ?, ?, ?)
#             """,
#             values,
#         )
#         conn.commit()
#     finally:
#         conn.close()
def save_record(session_id, record):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history (session_id, text, score, label, pinyin, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?)",
        [session_id, record["text"], record["score"],
         record["label"], record["pinyin"], record["created_at"]],
    )
    conn.commit()
    conn.close()

# def get_history(limit): #更换5
#     records = load_history()  # 读出文件里的全部记录
#     records.reverse()  # 倒过来：新的排前面
#     return records[:limit]  # 切一刀：返回指定数量的记录。
# def get_history(limit):
#     conn = get_conn()
#     cur = conn.cursor()
#     rows = cur.execute(
#         "SELECT * FROM history ORDER BY created_at DESC LIMIT ?",
#         [limit],
#     ).fetchall()
#     conn.close()

#     records = []
#     for row in rows:
#         records.append(dict(row))
#     return records
def get_history(session_id, limit):
    conn = get_conn()
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT * FROM history WHERE session_id = ? ORDER BY created_at DESC LIMIT ?",
        [session_id, limit],
    ).fetchall()
    conn.close()

    records = []
    for row in rows:
        records.append(dict(row))
    return records
