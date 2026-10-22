"""生成演示用的合成数据

为什么需要它：
1. 真实教学数据涉及学生隐私，不能进仓库
2. 评审需要能一键复现出可演示的数据集
3. 固定随机种子 → 任何人重跑都得到完全相同的成绩，可复现

输出：
    data/seed/课程大纲_合成.md
    data/seed/题目清单_合成.csv
    data/seed/成绩表_合成.xlsx

跑法：
    .venv/Scripts/python.exe scripts/make_seed.py
"""

from __future__ import annotations

import random
from pathlib import Path

import pandas as pd

SEED = 20261022
OUT = Path(__file__).resolve().parent.parent / "data" / "seed"

OBJECTIVES = [
    ("CO1", "掌握数据结构的基本概念与复杂度分析方法"),
    ("CO2", "能够针对具体问题选择合适的算法并实现"),
    ("CO3", "能够对算法正确性与效率进行分析与评价"),
]

# (题号, 主要支撑的目标, 满分, 难度 0-1 越高越难)
QUESTIONS = [
    ("Q1", "CO1", 10, 0.20),
    ("Q2", "CO1", 10, 0.30),
    ("Q3", "CO2", 15, 0.50),
    ("Q4", "CO2", 15, 0.60),
    ("Q5", "CO2", 10, 0.45),
    ("Q6", "CO3", 15, 0.72),
    ("Q7", "CO3", 15, 0.88),
    ("Q8", "CO3", 10, 0.65),
]

N_STUDENTS = 40


def main() -> None:
    rng = random.Random(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------- 课程大纲
    outline = ["# 数据结构与算法 · 课程教学大纲（合成数据）", ""]
    outline.append("> 本文件为演示用合成数据，不对应任何真实课程、教师或学生。")
    outline.append("")
    outline.append("## 课程目标")
    outline.append("")
    for oid, text in OBJECTIVES:
        outline.append(f"- **{oid}**　{text}")
    outline.append("")
    outline.append("## 考核方式")
    outline.append("")
    outline.append("闭卷考试，共 8 道题，总分 100 分。各题支撑的课程目标见题目清单。")
    outline.append("")
    outline.append("## 达成度评价方法")
    outline.append("")
    outline.append("各课程目标达成度 = 该目标下所有考核点得分率按满分加权平均。")
    (OUT / "课程大纲_合成.md").write_text("\n".join(outline), encoding="utf-8")

    # ---------------------------------------------------------- 题目清单
    qdf = pd.DataFrame(
        [
            {
                "题号": qid,
                "支撑课程目标": oid,
                "满分": mark,
                "难度系数": difficulty,
                "考核要求": f"第 {qid[1:]} 题考核要求（合成数据）",
            }
            for qid, oid, mark, difficulty in QUESTIONS
        ]
    )
    qdf.to_csv(OUT / "题目清单_合成.csv", index=False, encoding="utf-8-sig")

    # ---------------------------------------------------------- 成绩表
    rows = []
    for i in range(1, N_STUDENTS + 1):
        # 每个学生有自己的能力水平，正态分布
        ability = min(0.98, max(0.30, rng.gauss(0.71, 0.10)))
        row: dict[str, object] = {"学号": f"SYN{i:03d}", "姓名": f"合成学生{i:02d}"}
        for qid, _oid, mark, difficulty in QUESTIONS:
            # 以难度 0.5 为基准线：越简单得分率越高，越难越低
            rate = ability - (difficulty - 0.5) * 0.32 + rng.gauss(0, 0.06)
            rate = min(1.0, max(0.0, rate))
            row[qid] = round(rate * mark, 1)
        rows.append(row)

    sdf = pd.DataFrame(rows)
    sdf.to_excel(OUT / "成绩表_合成.xlsx", index=False)

    # ---------------------------------------------------------- 汇总
    total_full = sum(m for _, _, m, _ in QUESTIONS)
    avg_total = sum(sum(sdf[q].tolist()) for q, _, _, _ in QUESTIONS) / N_STUDENTS
    print(f"已生成 {len(sdf)} 名学生 × {len(QUESTIONS)} 道题（总分 {total_full}）")
    print(f"班级平均分：{avg_total:.1f} / {total_full}")
    for oid, _ in OBJECTIVES:
        qs = [q for q, o, _, _ in QUESTIONS if o == oid]
        got = sum(sum(sdf[q].tolist()) for q in qs)
        full = sum(m for q, _, m, _ in QUESTIONS if q in qs) * N_STUDENTS
        print(f"  {oid}：{got / full:.3f}（{len(qs)} 道题）")
    print(f"\n输出目录：{OUT}")


if __name__ == "__main__":
    main()
