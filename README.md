# SmartHub_TEST / MiniTask

这是一个专门用于测试 **SmartHub AI 自动化测试平台** 的小型靶场项目。

业务链路很短：登录 → 项目管理 → 任务管理 → 状态流转 → 搜索筛选 → 仪表盘统计。项目内保留确定性缺陷和独立评估基线，可用于验证 SmartHub 的需求理解、测试设计、知识库检索、API/UI 自动执行、缺陷发现与测试报告能力。

## 技术栈
- Frontend: Vue 3 + Vite + Vue Router
- Backend: FastAPI + SQLite
- Deploy: Docker Compose

## 一键启动
```bash
docker compose up -d --build
```

访问：
- Web: http://localhost:8080
- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/api/health

演示账号：
```text
admin / admin123
```

## 推荐 SmartHub 输入

### 1. 当前版本正式需求
盲测时只把下面文件作为当前 ProjectVersion 的正式需求输入：
```text
docs/requirements.md
```

在 SmartHub 中建议放到：
```text
workspace/branches/{version}/input/requirements/
```

### 2. 共享知识库
将本仓库 `knowledge/` 下的知识资料导入 SmartHub：
```text
workspace/shared/knowledge/
```

这些资料只提供测试方法、历史风险和执行经验，不是当前版本的正式需求，也不包含预埋缺陷答案。

### 3. 不要提供给 Agent 的评估答案
盲测期间不要把下面文件提供给 Agent：
```text
docs/seed-bugs.md
docs/test-baseline.md
docs/knowledge-benchmark.md
```

## 推荐对照实验

执行两轮相同需求：

```text
A 组：只提供 requirements.md
B 组：requirements.md + knowledge/
```

重点对比：
- 测试点/测试用例数量与拆分粒度
- 边界、状态机、数据一致性、查询组合、统计校验覆盖率
- 知识场景命中率
- 预埋 Bug 命中率
- API/UI 脚本一次通过率
- 误报率与漏报率

SmartHub 当前 PlanningAgent 可在同一 Planning Session 中连续完成需求理解和测试设计；知识库应主要用于补充“怎么测、哪些风险容易漏”。正式执行仍应以发布后的 TestCase/TestExecutionHandoff 为准，知识不得覆盖正式 Expected Result。

## 目录
```text
backend/                         FastAPI API
frontend/                        Vue3 UI
docs/requirements.md             当前版本被测需求
docs/seed-bugs.md                隐藏缺陷基准答案
docs/test-baseline.md            最小测试覆盖参考
docs/knowledge-benchmark.md      知识库增益评估方法
knowledge/                       导入 workspace/shared/knowledge 的共享知识
```

## 重置数据
```bash
docker compose down -v
docker compose up -d --build
```
