"""模块 1 · 材料解析

三个入口函数，统一返回 (结果, 错误信息) 二元组：
    成功 → (结果, None)
    失败 → (None, "给用户看的中文说明")

设计约定（写进 P05，后续改动必须遵守）：
1. 绝不向上抛异常 —— 页面层不应该出现 traceback
2. 只依赖 pdfplumber / python-docx / openpyxl，不引入新依赖
3. 文本保留段落分隔，不要把整篇压成一行

状态：待实现（10/25 - 10/26）
调用约束模板见《零基础起飞》第 4 天。
"""

from __future__ import annotations

from pathlib import Path


def parse_pdf(path: str | Path) -> tuple[str | None, str | None]:
    """从 PDF 抽取纯文本（含扫描件时降级提示）。"""
    raise NotImplementedError("待实现：P05-parse")


def parse_docx(path: str | Path) -> tuple[str | None, str | None]:
    """从 DOCX 抽取纯文本。"""
    raise NotImplementedError("待实现：P05-parse")


def parse_excel(path: str | Path) -> tuple[list[dict] | None, str | None]:
    """把 Excel 第一个工作表读成 list[dict]，表头作为 key。"""
    raise NotImplementedError("待实现：P05-parse")
