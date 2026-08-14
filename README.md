# SmartHub_TEST / MiniTask

这是一个专门用于测试 **SmartHub AI 自动化测试平台** 的小型靶场项目。

业务链路很短：登录 → 项目管理 → 任务管理 → 状态流转 → 搜索筛选 → 仪表盘统计，但项目内预埋了 7 个确定性缺陷，可用于验证 SmartHub 的需求分析、测试设计、API/UI 自动执行、缺陷发现与测试报告能力。

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
盲测时只给 SmartHub：
```text
docs/requirements.md
```
不要把 `docs/seed-bugs.md` 提供给 Agent，因为它是预埋缺陷的基准答案。

## 目录
```text
backend/               FastAPI API
frontend/              Vue3 UI
docs/requirements.md   被测需求
docs/seed-bugs.md      缺陷基准答案
docs/test-baseline.md  最小测试覆盖参考
```

## 重置数据
```bash
docker compose down -v
docker compose up -d --build
```
