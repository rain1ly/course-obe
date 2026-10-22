"""pytest 配置：让测试能从项目根导入 core 包。

没有这个文件时，pytest 只会把 tests/ 加入 sys.path，
`from core.domain import ...` 会报 ModuleNotFoundError。
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
