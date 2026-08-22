# SmartHub 知识库增益评估

> 这是评估文件，盲测时不要提供给 Agent。

## 目标

判断 SmartHub 的知识检索是否真正改善测试设计，而不是只发生了 `knowledge.search` Tool Call。

## 对照方式

使用同一组正式需求输入、同一模型配置和同一测试范围执行两组：

```text
正式输入：
- docs/requirements.md
- docs/api-spec.yaml

A：仅正式输入
B：正式输入 + knowledge/ 到 workspace/shared/knowledge
```

建议每组至少执行 2 次，降低生成式波动影响。

## 需要记录的指标

### 1. 知识检索命中

记录 PlanningAgent 是否检索到以下场景族：
- KS-VAL：输入边界/枚举
- KS-CRUD：CRUD/级联关系
- KS-STATE：状态机
- KS-DATA：跨入口一致性
- KS-QUERY：查询
- KS-STAT：统计
- KR：历史回归风险

只调用搜索但最终 TestPoint/TestCase 没吸收，不算有效命中。

### 2. 测试设计增益

重点观察 B 组相对 A 组是否增加：
- 空白字符串，而不仅是空字符串
- 每条状态边独立用例与非法回退
- 父资源删除后的子资源二次查询
- 每个枚举筛选值的准确性验证
- 非法枚举值
- 查询组合
- Dashboard 源数据反算
- UI/API 边界一致性

### 3. 缺陷命中增益

重点比较：

```text
Knowledge Uplift = B 组命中 Bug 数 - A 组命中 Bug 数
```

其中 BUG-09、BUG-10 专门用于观察边界/枚举知识是否被真正吸收。

### 4. 用例质量

不要只看用例总数，还需要记录：
- 需求覆盖率
- 知识场景覆盖率
- 重复用例比例
- 过度合并用例比例
- 不可执行用例比例
- 无正式依据的 Expected Result 数量

## 执行阶段边界

正式 TestCase 发布后，执行必须保持其业务断言。`knowledge/test-execution` 只可帮助脚本实现、测试数据、locator 和稳定性，不应该在执行时新增业务 Expected Result 或修改冻结 TestCase。

如果后续给 TestScriptAgent / FailureAnalysisAgent / ScriptRepairAgent 增加 `knowledge.search`、`knowledge.read_chunk`，建议单独统计：
- 执行知识检索率
- 首次脚本成功率变化
- 自愈成功率变化
- 因错误知识导致的断言语义漂移次数（应为 0）
