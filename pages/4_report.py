"""模块 4 · 可视化与报告导出

对应 Prompt：P13-report
状态：待实现（计划 11/4 - 11/7）

导出的必须是「真文件」，演示视频里要当场打开给人看。
"""

from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="04 生成报告", layout="wide")

st.title("04 · 生成报告")
st.caption("雷达图、达成度矩阵，以及可直接提交的 Word 报告")

st.info("模块尚未实现。计划 11/4 之后开始，届时先做图表、再做导出。")

st.markdown("**计划交付**")
st.markdown(
    "- 各课程目标达成度雷达图\n"
    "- 逐题得分率的分组柱状图\n"
    "- 一键导出 Word：封面 + 数据表 + 图表 + 改进建议草稿"
)

st.markdown("**验收标准**")
st.markdown(
    "- 导出的 docx 能被 Word 正常打开\n"
    "- 图表以图片形式嵌入，不出现裂图\n"
    "- 文件里不含任何学生姓名与学号"
)
