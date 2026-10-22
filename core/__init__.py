"""core —— 业务内核

分层约定（P01 确立，后续所有模块必须遵守）：

    core.schemas    数据结构与校验模型，不含逻辑
    core.parsers    文件 → 文本 / 表格
    core.ai_client  模型调用，只返回数据，不做业务计算
    core.domain     纯函数业务算法，禁止引入网络与数据库
    core.db         本地存储

依赖方向只允许单向：pages → core，core 内部不允许反向依赖 pages。
"""
