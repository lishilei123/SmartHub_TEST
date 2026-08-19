# MiniTask 预埋缺陷基准答案

> **注意：盲测 SmartHub 时不要把本文档提供给测试 Agent。**

| ID | 层级 | 预埋缺陷 | 期望发现方式 | 相关知识场景 |
|---|---|---|---|---|
| BUG-01 | API/安全 | `admin` 使用错误密码仍返回 200 和 token | 登录负向用例 | KE-API-002 |
| BUG-02 | API/功能 | 任务标题为空仍可创建 | 必填/边界校验 | KS-VAL-001 |
| BUG-03 | API/数据一致性 | 删除项目后其任务没有级联删除 | 父子资源删除闭环 | KS-CRUD-002 / KS-DATA-001 |
| BUG-04 | API/状态机 | completed 任务可回退到 in_progress/todo | 非法状态边 | KS-STATE-002 / KR-003 |
| BUG-05 | API/查询 | `priority=high` 实际返回 medium | 筛选准确性 | KS-QUERY-001 / KR-004 |
| BUG-06 | API/UI/统计 | Dashboard 已完成任务数固定多 1 | 源数据反算 | KS-STAT-001 / KR-005 |
| BUG-07 | UI | 删除项目没有二次确认 | UI 交互用例 | KE-UI-002 / KR-006 |
| BUG-08 | 前后端一致性 | UI 标题限制 50 字，后端无同等上限 | 双入口边界一致性 | KS-VAL-002 / KR-007 |
| BUG-09 | API/边界 | 项目名称只输入空格时先通过 Pydantic 非空校验，保存前 `strip()` 后变成空名称 | 空白字符串/规范化边界 | KS-VAL-001 / KR-001 |
| BUG-10 | API/参数校验 | 任务查询传非法 `status` / `priority` 时没有返回 400，而是按普通筛选返回 200 | 非法枚举参数 | KS-VAL-003 / KR-004 |

## 使用建议

1. A 组只给 SmartHub `docs/requirements.md`。
2. B 组额外加载 `knowledge/` 到 `workspace/shared/knowledge`。
3. 让 PlanningAgent 完成需求理解和测试设计，再执行 UI + API 测试。
4. 测试结束后再用本文档做命中率对照。
5. 建议记录：发现数、误报数、漏报数、知识场景覆盖率、自动生成脚本成功率、脚本自愈成功率。
