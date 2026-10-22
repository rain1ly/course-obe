"""模块 2 · 模型调用封装

职责：把「课程目标 + 题目」变成结构化的 MappingResult 列表。
边界：只返回数据，绝不做业务计算。

硬性约束（写进 P07，也是技术文档 4.2 的素材）：
1. 密钥只从环境变量读取，代码里不得出现任何字面量
2. 返回必须经 Pydantic 校验；失败时把错误信息带回去重试，最多 MAX_RETRIES 次
3. 全部失败时返回空列表，不抛异常 —— 由页面提示「全部转人工」
4. 单次调用超时 TIMEOUT_SECONDS
5. 禁止无界重试

状态：待实现（10/27 - 10/29）
"""

from __future__ import annotations

import os

from core.schemas import CourseObjective, MappingResult, Question

# 重试上限。选 2 而不选 5 的理由：单次调用约 3-8 秒，
# 2 次重试的最坏耗时约 30 秒，仍在用户可接受范围内；再多就是在消耗耐心。
MAX_RETRIES = 2

# 单次请求超时（秒）
TIMEOUT_SECONDS = 30


def is_configured() -> bool:
    """检查环境变量是否就绪，供页面做前置提示。"""
    return bool(os.getenv("OPENAI_API_KEY")) and bool(os.getenv("OPENAI_BASE_URL"))


def call_mapping(
    objectives: list[CourseObjective],
    questions: list[Question],
) -> list[MappingResult]:
    """让模型判断每道题支撑哪个课程目标。

    返回的每一条都必须带 confidence 与 evidence；
    confidence 低于 CONFIDENCE_THRESHOLD 的项，need_manual_review 置 True。
    """
    raise NotImplementedError("待实现：P07-mapping")
