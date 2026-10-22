"""数据结构与校验模型

设计原则（写进 P01 / 技术文档 4.2）：
1. extra="forbid" —— 模型多返回一个字段即视为失败，防止字段漂移
2. confidence 必须有界，evidence 必须短且可核对
3. 低置信度必须由模型自己标记为待人工确认，而不是由调用方猜

这一层的价值：模型输出先过这里，过不去就重试，过去了的才是可信数据。
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# 低于此阈值视为「模型没有把握」，必须转人工确认
CONFIDENCE_THRESHOLD = 0.6

# evidence 的长度上限：太长说明模型在复述题干而不是给依据
EVIDENCE_MAX_LEN = 200


class CourseObjective(BaseModel):
    """一条课程目标。"""

    model_config = ConfigDict(extra="forbid")

    objective_id: str = Field(..., description="课程目标编号，如 CO1")
    content: str = Field(..., description="课程目标原文")


class Question(BaseModel):
    """一道考核题目。"""

    model_config = ConfigDict(extra="forbid")

    question_id: str = Field(..., description="题号，如 Q3")
    content: str = Field(..., description="题干或考核要求")
    full_mark: float | None = Field(None, description="满分，未知则为 None")


class MappingResult(BaseModel):
    """一条「题目支撑某个课程目标」的判断。"""

    model_config = ConfigDict(extra="forbid")

    question_id: str
    objective_id: str
    confidence: float = Field(..., ge=0.0, le=1.0, description="模型自评把握程度")
    evidence: str = Field(..., max_length=EVIDENCE_MAX_LEN, description="判断依据，须取自题目原文")
    need_manual_review: bool = Field(
        False,
        description="confidence 低于阈值时置 True；由模型或调用方显式标记",
    )


class MappingResponse(BaseModel):
    """一次映射调用的完整返回。"""

    model_config = ConfigDict(extra="forbid")

    mappings: list[MappingResult] = Field(default_factory=list)
    notes: str = Field("", description="模型的补充说明，可为空")


def in_need_of_review(item: MappingResult) -> bool:
    """统一判断某条映射是否需要人工介入。

    单一出口，避免各页面各写一套阈值判断。
    """
    return item.need_manual_review or item.confidence < CONFIDENCE_THRESHOLD
