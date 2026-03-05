# 排障指南

## 连接与鉴权

- `CONNECTION_FAILED` / WebSocket 连接失败：
  - 检查 `HOMEASSISTANT_URL` 是否可达
  - 检查长期令牌 `HOMEASSISTANT_TOKEN` 是否有效
- `401 Unauthorized`：
  - Token 缺失或无效

## 工具级错误

- `Unknown tool: ha_automation_create`：
  - 属于预期行为，改用 `ha_config_set_automation`
- `ha_get_addon -> Unknown command`：
  - Add-on API 依赖 HA OS/Supervised Supervisor

## 自动化回调常见错误

- 事件名拼写错误 `notify_openclaw_agen`：
  - 正确值是 `notify_openclaw_agent`
  - 修正事件名后重新写入自动化

- 使用了 `triggers` / `actions` 但未做归一化：
  - `ha_config_set_automation` 的 payload 应使用 `trigger` / `action`
  - 写入前先做字段归一化

- 自动化事件名与插件配置不一致：
  - 检查插件 `agentEventType` 和 `directEventType`
  - 默认应分别为 `notify_openclaw_agent` 与 `notify_openclaw_direct`

- 用户要求原文不改写，但实际配置仍走 V2：
  - 将事件切换为 `notify_openclaw_direct`
  - 仅在允许改写/润色时才使用 V2

## 最小恢复序列

```bash
mcporter list server ha-mcp --schema
mcporter call server.ha_config_list_areas
mcporter call server.ha_get_overview detail_level:minimal
```
