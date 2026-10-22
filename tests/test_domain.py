"""达成度算法的单元测试

这是全项目的「免死金牌」：只要这些测试是绿的，你就有资格对评委说
「计算部分我验证过，它可复现」。

跑法：
    .venv/Scripts/python.exe -m pytest tests/ -v
"""

from __future__ import annotations

from core.domain import (
    THRESHOLD_BASIC,
    THRESHOLD_REACHED,
    build_report,
    classify,
    objective_attainment,
    question_score_rates,
)
from core.schemas import MappingResult


def mk(qid: str, oid: str, conf: float = 0.9) -> MappingResult:
    """构造一条映射，减少测试噪音。"""
    return MappingResult(
        question_id=qid,
        objective_id=oid,
        confidence=conf,
        evidence="测试用",
    )


# ---------------------------------------------------------------- 核心算法
def test_single_objective_single_question():
    """一道题、一个目标：达成度就是平均得分率。"""
    result = objective_attainment(
        [mk("Q1", "CO1")],
        scores={"Q1": [8, 8, 8]},
        full_marks={"Q1": 10},
    )
    assert result["CO1"] == 0.8


def test_two_objectives_are_independent():
    result = objective_attainment(
        [mk("Q1", "CO1"), mk("Q2", "CO2")],
        scores={"Q1": [10, 10], "Q2": [5, 5]},
        full_marks={"Q1": 10, "Q2": 10},
    )
    assert result["CO1"] == 1.0
    assert result["CO2"] == 0.5


def test_weighted_by_full_mark():
    """满分高的题权重更大：0.5*10 + 0.9*90 的分母是 100，不是 2。"""
    result = objective_attainment(
        [mk("Q1", "CO1"), mk("Q2", "CO1")],
        scores={"Q1": [5], "Q2": [81]},
        full_marks={"Q1": 10, "Q2": 90},
    )
    assert abs(result["CO1"] - 0.86) < 1e-9


def test_duplicate_mapping_not_double_counted():
    """同一题重复映射到同一目标，不能重复加权。"""
    result = objective_attainment(
        [mk("Q1", "CO1"), mk("Q1", "CO1")],
        scores={"Q1": [6]},
        full_marks={"Q1": 10},
    )
    assert result["CO1"] == 0.6


def test_zero_full_mark_is_skipped():
    """满分为 0 的题目跳过，而不是除零崩溃。"""
    rates = question_score_rates({"Q1": [3]}, {"Q1": 0})
    assert rates == {}


def test_objective_without_questions_absent():
    """没有题目支撑的目标不出现在结果里 —— 不伪造 0。"""
    result = objective_attainment(
        [mk("Q1", "CO1")],
        scores={"Q1": [10]},
        full_marks={"Q1": 10},
    )
    assert "CO2" not in result


def test_empty_input_returns_empty():
    assert objective_attainment([], {}, {}) == {}


# ---------------------------------------------------------------- 分级
def test_classify_thresholds():
    assert classify(THRESHOLD_REACHED) == "达成"
    assert classify(THRESHOLD_REACHED - 0.001) == "基本达成"
    assert classify(THRESHOLD_BASIC) == "基本达成"
    assert classify(THRESHOLD_BASIC - 0.001) == "未达成"


# ---------------------------------------------------------------- 报告
def test_build_report_sorted_ascending():
    """报告按达成度升序，最差的目标排最前，方便教师先看问题。"""
    report = build_report(
        [mk("Q1", "CO1"), mk("Q2", "CO2")],
        scores={"Q1": [9], "Q2": [5]},
        full_marks={"Q1": 10, "Q2": 10},
    )
    assert [r.objective_id for r in report] == ["CO2", "CO1"]
    assert report[0].level == "未达成"
    assert report[1].percent == 90.0


def test_build_report_counts_marked_questions():
    report = build_report(
        [mk("Q1", "CO1"), mk("Q2", "CO1")],
        scores={"Q1": [5], "Q2": [5]},
        full_marks={"Q1": 10, "Q2": 20},
    )
    assert report[0].question_ids == ["Q1", "Q2"]
    assert report[0].total_full_mark == 30
