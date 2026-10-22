"""模块 3 · 达成度计算

对应 Prompt：P11-domain
状态：待实现（计划 11/1 - 11/3）

注意：本页不调用任何 AI。全部计算由 core/domain.py 的纯函数完成，
可单测、可复算、可解释 —— 这是「结果可验证」的落点。
"""

from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="03 达成度计算", layout="wide")

st.title("03 · 达成度计算")
st.caption("确定性算法：同样的输入必然得到同样的输出")

st.info("模块尚未实现。`core/domain.py` 已有最小实现与单测，接下来把页面接上去。")

st.markdown("**计划交付**")
st.markdown(
    "- 按确认后的映射计算每个课程目标的达成度\n"
    "- 展示每个目标的支撑题目与权重构成\n"
    "- 达成 / 基本达成 / 未达成的分级，阈值可调"
)

st.markdown("**为什么不用 AI 算**")
st.markdown(
    "教师需要向督导组解释分数怎么来的。模型不保证确定性，"
    "而一行可测的算法可以逐步追溯 —— 这个取舍已记录在 "
    "`decisions/ADR-001-为什么用确定性算法算达成度.md`。"
)
