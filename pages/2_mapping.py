"""模块 2 · AI 语义映射 + 人工确认

对应 Prompt：P07-mapping
状态：待实现（计划 10/27 - 10/29）

这一页是整个项目的核心：模型只给建议，人做最终决定。
"""

from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="02 AI 映射", layout="wide")

st.title("02 · 题目与课程目标的映射")
st.caption("模型给出候选匹配、置信度和原文依据；你确认之后才进入计算")

st.info("模块尚未实现。先让 AI 按《零基础起飞》第 6 天填 `core/schemas.py` 与 `core/ai_client.py`。")

st.markdown("**计划交付**")
st.markdown(
    "- 一键为全部题目生成映射建议\n"
    "- 每条建议都带 confidence 与 evidence\n"
    "- 置信度低于 0.6 的项高亮，要求人工确认\n"
    "- 可编辑的映射表，确认状态落库"
)

st.markdown("**设计红线**")
st.markdown(
    "- 模型不得直接给出达成度数值，只给映射关系\n"
    "- 校验失败重试上限 2 次，全失败则全量转人工\n"
    "- 任何情况下都不把异常抛到页面"
)
