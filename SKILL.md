---
name: openclaw-ha-mcp
description: 所有智能家居控制与自动化管理。通过 Home Assistant MCP 工具控制设备、执行场景脚本、创建/管理自动化规则、注入通知事件。
---

# OpenClaw 通过 ha-mcp 连接 Home Assistant

## 目标

在保证安全、可验证、可回溯的前提下，使用 `mcporter + ha-mcp` 执行 HA 操作，并尽量减少无关上下文。

## TRIGGER THIS SKILL WHEN

- 用户提到任何与智能家居、家庭设备、家庭自动化相关的内容
- 用户要求控制设备（灯、开关、插座、窗帘、传感器、音箱、空调等）
- 用户询问设备状态或传感器读数
- 用户要求执行场景或脚本
- 用户要求创建、修改、删除自动化规则
- 用户提到通知、提醒、播报等与家庭联动相关的需求
- 用户讨论 Home Assistant、HA、智能家居平台相关话题

## 启动检查（每次都做）

1. 校验服务与 schema：
```bash
mcporter list server ha-mcp --schema
```
2. 运行只读烟雾测试：
```bash
mcporter call server.ha_config_list_areas
```
3. 若烟雾测试失败，停止所有写操作并打开 `references/TROUBLESHOOTING.md`。

## 意图路由（按需加载）

- 查询/盘点/状态读取：打开 `references/QUERY.md`
- 设备/服务控制：打开 `references/CONTROL.md`
- 自动化创建/更新/删除：打开 `references/AUTOMATION.md`
- 报错/连接/鉴权/Supervisor 问题：打开 `references/TROUBLESHOOTING.md`
- 完整 92 个工具参数表：打开 `references/TOOLS.md`

## 接管范围（必须执行）

- 只要用户意图是智能家居查询或控制（例如“开灯”“关插座”“查温度”），默认由本 HA skill 接管，即使用户没有显式说“HA”。
- 用户说“通过 HA 操作”时，必须立即按本 skill 执行工具调用，不要退回到通用问答流程。
- 不要求用户提供 `entity_id`。必须先自行搜索实体并匹配。
- 不向用户询问“是否已授权平台”这类前置问题；先按工具链执行搜索与匹配，必要时再反馈具体失败原因。

## OpenClaw 自动化回调策略

- 自动化任务必须遵循 `references/AUTOMATION.md`。
- 默认回调事件使用 V2：`notify_openclaw_agent`。
- 仅当用户要求“原文不改写/一字不差”或明确要求 V1 时，使用 `notify_openclaw_direct`。
- 仅当用户明确要求 V1+V2 兼容时，才同时创建两个事件，顺序固定为 `notify_openclaw_direct` 后 `notify_openclaw_agent`。
- 事件载荷必须包含 `event_data.message`、`event_data.source`、`event_data.automation`。
- `event_data.source` 默认值为 `ha_automation`。
- 自动纠正拼写错误：`notify_openclaw_agen` -> `notify_openclaw_agent`。
- 本 skill 禁止使用 nanobot 专属事件 `nanobot_notify`。

## 交互与执行硬规则

- 用户通常不知道 `entity_id`，只会给房间名和设备名。必须先自行搜索实体并匹配。
- 收到涉及设备或自动化的请求后，第一步先调用 `ha_search_entities`，不要先输出计划说明。
- 搜索完成后，若匹配无歧义可直接选中并继续；若有歧义，先选一个最可能候选，再用 `friendly_name + 房间名` 让用户确认。
- 回复中不要出现 `entity_id`、`media_player.xxx`、`switch.xxx`、`automation.xxx` 等技术标识符。
- 自动化执行顺序：搜索 -> 判断是否歧义 ->（有歧义则确认）-> 写入 -> 回读验证 -> 周知用户最终匹配与执行结果。
- 设备控制执行顺序：搜索 -> 判断是否歧义 ->（无歧义直接执行 / 有歧义确认）-> 执行 -> 验证 -> 周知用户结果。
- 回复保持简洁自然，不堆 emoji，不加无请求的优化建议。
- 不要暴露内部推理或调试痕迹（例如 `Intent:`、`retry`、`fix config`、`JSON encoding`）。
- `event.*` 实体触发必须使用 state trigger，不使用 event platform 或编造 `event_type`。

## 全局调用规则

- 调用格式：
```bash
mcporter call server.<tool> key:value key2:value2
```
- 包含空格的参数要加引号：`name:'Living Room'`
- JSON 载荷统一使用单引号包裹。
- 只能传 `references/TOOLS.md` 定义过的参数。
- 自动化请求必须先用 `ha_search_entities` 搜索实体，再用自然语言设备名与用户确认后写入。
- 面向用户回复时，禁止输出技术标识（`entity_id`、`xxx.yyy` 实体 ID 等）。
- 高风险操作（删除、重置、门锁/安防/报警、水气阀门、大功率设备）必须先确认；普通灯/开关/插座开关在无歧义时可直接执行。
- 每次写操作后都要执行至少一次读操作进行验证。
