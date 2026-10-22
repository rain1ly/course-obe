"""元素 3 的内核 · 达成度计算

这一层是全项目唯一「不依赖 AI」的部分：
纯函数、无网络、无数据库、无随机性 —— 同样的输入必然得到同样的输出。

为什么重要（写进技术文档第 5 章）：
教师要向督导组解释分数怎么来的。模型给不出可追溯的计算过程，
但一个可单测的纯函数可以。

公式：
    attainment(CO) = Σ_题目 Σ_学生 得分 / Σ_题目 (学生数 × 满分)

即该目标下所有考核点得分率按满分加权平均。
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.schemas import MappingResult

# 达成度分级阈值。各校标准不同，做成模块级常量便于统一调整。
THRESHOLD_REACHED = 0.65  # 达成
THRESHOLD_BASIC = 0.60  # 基本达成


@dataclass
class ObjectiveReport:
    """单个课程目标的达成情况。"""

    objective_id: str
    attainment: float
    level: str
    question_ids: list[str] = field(default_factory=list)
    total_full_mark: float = 0.0

    @property
    def percent(self) -> float:
        return round(self.attainment * 100, 1)


def _dedup(mappings: list[MappingResult]) -> list[MappingResult]:
    """去掉空编号与重复的「题目-目标」配对。

    重复映射会让同一道题被重复加权，必须先去重，否则结果偏高。
    """
    seen: set[tuple[str, str]] = set()
    out: list[MappingResult] = []
    for m in mappings:
        if not m.question_id or not m.objective_id:
            continue
        key = (m.question_id, m.objective_id)
        if key in seen:
            continue
        seen.add(key)
        out.append(m)
    return out


def question_score_rates(
    scores: dict[str, list[float]],
    full_marks: dict[str, float],
) -> dict[str, float]:
    """每题的平均得分率。

    满分缺失或为 0 的题目直接跳过 —— 宁可少算，不可除零。
    """
    rates: dict[str, float] = {}
    for qid, marks in full_marks.items():
        if marks is None or marks <= 0:
            continue
        got = scores.get(qid) or []
        if not got:
            continue
        rates[qid] = sum(got) / (len(got) * marks)
    return rates


def objective_attainment(
    mappings: list[MappingResult],
    scores: dict[str, list[float]],
    full_marks: dict[str, float],
) -> dict[str, float]:
    """各课程目标的达成度，返回 {目标编号: 0~1 之间的值}。

    没有题目支撑的目标不会出现在结果里 —— 这本身就是需要提醒教师的信息，
    由页面层负责提示，而不是在这里伪造一个 0。
    """
    rates = question_score_rates(scores, full_marks)

    buckets: dict[str, list[tuple[float, float]]] = {}
    for m in _dedup(mappings):
        if m.question_id not in rates:
            continue
        weight = full_marks[m.question_id]
        buckets.setdefault(m.objective_id, []).append((rates[m.question_id], weight))

    result: dict[str, float] = {}
    for oid, items in buckets.items():
        total_weight = sum(w for _, w in items)
        if total_weight <= 0:
            continue
        result[oid] = sum(rate * w for rate, w in items) / total_weight
    return result


def classify(value: float) -> str:
    """按阈值给达成度分级。"""
    if value >= THRESHOLD_REACHED:
        return "达成"
    if value >= THRESHOLD_BASIC:
        return "基本达成"
    return "未达成"


def build_report(
    mappings: list[MappingResult],
    scores: dict[str, list[float]],
    full_marks: dict[str, float],
) -> list[ObjectiveReport]:
    """生成可直接给页面渲染的报告明细，按达成度升序（先看没达成的）。"""
    values = objective_attainment(mappings, scores, full_marks)

    by_objective: dict[str, list[str]] = {}
    for m in _dedup(mappings):
        by_objective.setdefault(m.objective_id, []).append(m.question_id)

    reports = [
        ObjectiveReport(
            objective_id=oid,
            attainment=value,
            level=classify(value),
            question_ids=sorted(by_objective.get(oid, [])),
            total_full_mark=sum(full_marks.get(q, 0.0) for q in by_objective.get(oid, [])),
        )
        for oid, value in values.items()
    ]
    return sorted(reports, key=lambda r: r.attainment)
