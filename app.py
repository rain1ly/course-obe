"""达成度 · CourseOBE —— 首页

课程目标达成度智能分析工作台
2026 第九届传智杯 · AI 创新应用挑战赛 · 个人赛

设计约定：
- 本文件只负责首页展示，不放业务逻辑
- 业务逻辑一律在 core/ 下，页面只做编排
"""

from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="达成度 · CourseOBE",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------- 标题区
st.title("达成度 · CourseOBE")

st.markdown(
    "#### 把教师每学期要做一次的课程目标达成度评价，从 4 小时的 Excel 手工，变成 12 分钟。"
)

st.caption(
    "AI 只做语义映射，算法只做数值计算 —— 一份可审计、可复现的达成度报告。"
)

st.divider()

# ---------------------------------------------------------------- 工作流程
st.subheader("工作流程")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("### 01 上传材料")
    st.write("课程大纲、试卷题目、学生成绩表，一次拖进来。")

with c2:
    st.markdown("### 02 AI 映射")
    st.write("自动给出「题目 ↔ 课程目标」的候选匹配，附置信度与原文依据。")

with c3:
    st.markdown("### 03 人工确认")
    st.write("只处理低置信度的项。你确认过，才算数。")

with c4:
    st.markdown("### 04 生成报告")
    st.write("雷达图与达成度矩阵，一键导出可提交的 Word 报告。")

st.divider()

# ---------------------------------------------------------------- 进度区
st.subheader("当前进度")

left, right = st.columns([3, 2])

with left:
    st.markdown("**阶段：骨架搭建完成 · v0.1.0-dev**")
    st.progress(10, text="10% · 环境与架构就绪")
    st.markdown(
        "- [x] 虚拟环境与依赖\n"
        "- [x] 目录骨架与分层约定\n"
        "- [ ] 模块 1 · 材料解析\n"
        "- [ ] 模块 2 · AI 语义映射\n"
        "- [ ] 模块 3 · 达成度计算\n"
        "- [ ] 模块 4 · 报告导出"
    )

with right:
    st.markdown("**下一步**")
    st.info(
        "按《零基础起飞》第 4 天的任务，让 AI 填充 `core/parsers.py`，"
        "再把「材料上传」页接上去。"
    )
    st.markdown("**关键日期**")
    st.markdown("省赛作品提交：**2026-11-18**")

st.divider()

st.caption(
    "数据仅在本机处理，学生信息默认脱敏。演示数据见 data/seed/，已标注为合成数据。"
)
