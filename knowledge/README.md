# MiniTask 测试知识库

本目录用于验证 SmartHub 的知识库检索是否能实际提升测试设计质量。

导入 SmartHub 时，建议把本目录下的分类文件放到：

```text
workspace/shared/knowledge/
```

## 内容边界

知识库只保存三类内容：

1. **测试场景知识**：告诉 PlanningAgent 某类需求通常还要从哪些角度拆测试。
2. **测试执行知识**：告诉自动化执行如何准备数据、定位元素、校验结果和清理环境。
3. **历史风险知识**：保存过去容易回归的风险模式，用于提高测试优先级。

知识库不保存：
- 当前版本正式 Expected Result
- 当前版本预埋 Bug 答案
- 隐藏账号、Token、环境地址
- 用来绕过正式 TestCase 的临时执行规则

## 文件

```text
test-scenarios/input-boundary-and-enum.md
test-scenarios/crud-state-consistency.md
test-scenarios/query-and-statistics.md
test-execution/api-ui-automation.md
historical-risks/regression-patterns.md
```

每条知识使用稳定的场景 ID，便于后续统计 TestPoint/TestCase 是否真正吸收了检索结果。
