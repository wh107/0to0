#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 16:25:14 2026

@author: Administrator
"""

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from pypinyin import lazy_pinyin, Style  # 三方库nlp
from snownlp import SnowNLP  # 三方库nlp

import json  # 标准库
from datetime import datetime, timezone  # 标准库

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


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


profile = {
    "heroTitle": "关于我",
    "heroSubtitle": "项目，创意，灵感，心得，我的作品",
    "featuredWork": {
        "kicker": "作品",
        "title": "文字实验室",
        "copy": "拼音和情绪，挖掘中文里的细节",
        "linkLabel": "打开作品",
    },
    "identity": {
        "motto": "已识乾坤大，尤怜草木青",
        "learning": "零到全栈",
    },
}


def score_label(score):
    if score >= 0.6:
        return "偏积极"
    elif score <= 0.4:
        return "偏消极"
    else:
        return "中性"


class AnalyzeRequest(BaseModel):
    text: str


@app.get("/api/profile")
def get_profile():
    return profile


@app.post("/api/analyze")
def analyze(req: AnalyzeRequest):
    text = req.text
    score = round(SnowNLP(text).sentiments, 2)  # 真模型打的分
    result = {
        "text": req.text,
        "score": score,
        "label": score_label(score),
        "pinyin": " ".join(
            lazy_pinyin(text, style=Style.TONE)
        ),  # 真拼音，带声调,
        "created_at": datetime.now(timezone.utc).isoformat(
            timespec="seconds"
        ),  # ← 新增
    }
    save_record(result)  # ← 存档到文件
    return result


@app.get("/api/history")
def history():
    records = load_history()  # 读出文件里的全部记录
    records.reverse()  # 倒过来：新的排前面
    return records[:2]  # 切一刀：只留最近 10 条
