"""模块 1 · 材料上传与解析

对应 Prompt：P05-parse
状态：待实现（计划 10/25 - 10/26）
"""

from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="01 材料上传", layout="wide")

st.title("01 · 材料上传")
st.caption("课程大纲（PDF / DOCX）· 试卷题目（PDF / 图片 / 文本）· 学生成绩表（Excel）")

st.info("模块尚未实现。先让 AI 填充 `core/parsers.py`，再把上传与预览接上这一页。")

st.markdown("**计划交付**")
st.markdown(
    "- 三种文件的上传、解析与结果预览\n"
    "- 解析失败时给出中文说明，页面不出现 traceback\n"
    "- 上传过的材料落库，刷新不丢"
)

st.markdown("**验收标准**")
st.markdown(
    "- 三种文件都能解析出完整文本\n"
    "- 传一个不存在的文件 → 不崩溃\n"
    "- 把 .txt 改名成 .pdf 传进来 → 不崩溃"
)
