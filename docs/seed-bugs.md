# MiniTask 预埋缺陷基准答案

> **注意：盲测 SmartHub 时不要把本文档提供给测试 Agent。**

| ID | 层级 | 预埋缺陷 | 期望发现方式 |
|---|---|---|---|
| BUG-01 | API/安全 | `admin` 使用错误密码仍返回 200 和 token | 登录负向用例 |
| BUG-02 | API/功能 | 任务标题为空仍可创建 | 边界/必填校验 |
| BUG-03 | API/数据一致性 | 删除项目后其任务没有级联删除 | 数据关联用例 |
| BUG-04 | API/状态机 | completed 任务可回退到 in_progress/todo | 状态流转用例 |
| BUG-05 | API/查询 | `priority=high` 实际返回 medium | 筛选准确性 |
| BUG-06 | API/UI/统计 | Dashboard 已完成任务数固定多 1 | 数据核对 |
| BUG-07 | UI | 删除项目没有二次确认 | UI 交互用例 |
| BUG-08 | 前后端一致性 | UI 标题限制 50 字，后端无同等上限 | 边界一致性 |

## 使用建议

1. 给 SmartHub `docs/requirements.md`。
2. 让它生成测试用例并执行 UI + API 测试。
3. 测试结束后再用本文档做命中率对照。
4. 建议记录：发现数、误报数、漏报数、自动生成脚本成功率、脚本自愈成功率。
