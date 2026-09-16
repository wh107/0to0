# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 11:33:34 2026

@author: Administrator
"""

import json  # 标准库

# 定义用于存储内容的json文件
HISTORY_FILE = "history.json"

# 读文件
def load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# 先读出文件，再添加，最后写数据到文件
def save_record(record):
    records = load_history()
    records.append(record)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def get_history(limit):
    records = load_history()  # 读出文件里的全部记录
    records.reverse()  # 倒过来：新的排前面
    return records[:limit]  # 切一刀：返回指定数量的记录。