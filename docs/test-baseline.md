# MiniTask 最小测试基线

这不是完整测试脚本，而是用于判断 SmartHub 测试设计是否覆盖核心面的最小基线。

## 冒烟
- health 返回 200
- 正确账号登录成功
- 项目列表可访问
- 可创建项目和任务
- Dashboard 可加载

## 功能
- 登录正确/错误密码
- 项目 CRUD + 删除确认 + 级联关系
- 任务 CRUD
- 任务标题必填与长度边界
- todo → in_progress → completed 单向流转
- completed 禁止回退
- status / priority / keyword 查询组合
- Dashboard 统计值与任务真实数据一致

## API
- 未携带 token 返回 401
- 非法 status / priority 返回 400
- 不存在资源返回 404
- 创建返回 201，查询/修改/删除状态码符合约定

## UI
- 登录与退出
- 项目创建、改名、删除
- 项目跳转任务页
- 任务新增、筛选、状态推进、删除
- Dashboard 数字展示

## SmartHub 评估指标建议
- 需求点覆盖率
- 预埋 Bug 命中率
- 误报率 / 漏报率
- API 脚本一次通过率
- UI 脚本一次通过率
- UI Locator 变化后的自愈成功率
