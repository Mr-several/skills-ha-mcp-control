# 排障指南

## 连接与鉴权

- `CONNECTION_FAILED` / WebSocket 连接失败：
  - 检查 `HOMEASSISTANT_URL` 是否可达
  - 检查长期令牌 `HOMEASSISTANT_TOKEN` 是否有效
- `401 Unauthorized`：
  - Token 缺失或无效

## 工具级错误

- `Unknown tool: ha_automation_create` 或 `Unknown tool: ha_create_automation`：
  - 属于预期行为，改用 `ha_config_set_automation`
  - 先执行 `mcporter list server ha-mcp --schema` 确认当前工具集，再重试
  - 只有 `ha_config_get_automation` 回读成功后，才可对用户宣称“已创建成功”
- `ha_get_addon -> Unknown command`：
  - Add-on API 依赖 HA OS/Supervised Supervisor
- `notify.send_message` 用于“播放音乐”返回 400：
  - 根因：该接口更适合文字播报，不稳定支持音乐播放队列控制
  - 修复：改用音箱原生媒体控制 `media_player.*`
  - 推荐顺序：
    - 有明确媒体内容 -> `media_player.play_media`
    - 无明确媒体内容但要继续播放 -> `media_player.media_play`
  - 预防：执行前先检查设备是否有原生控制服务（`ha_list_services`）

## 自动化动作格式错误

- 使用 `action: event.fire` 发送 OpenClaw 通知：
  - 根因：`event.fire` 是 HA 服务调用，不是自动化的原生事件动作
  - 修复：将 `action: event.fire` + `data.event_type` 替换为 `event:` 键 + `event_data:`
  - 正确写法：
    ```yaml
    - event: notify_openclaw_agent
      event_data:
        message: ...
        source: ha_automation
        automation: ...
    ```

- 使用 `media_player.play_media` + `announce` 播报文字：
  - 根因：小米音箱不稳定支持 `media_content_type: announce`
  - 修复：改用 `notify.send_message` + `target.device_id`
  - 注意：需要 `device_id` 而非 `entity_id`，先用 `ha_get_device` 获取

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
  - 仅在允许改写或润色时才使用 V2

- 使用了 HA 原生通知服务（如 `notify.notify`、`persistent_notification.create`）通知用户：
  - 所有面向用户的通知必须走 OpenClaw 事件
  - 删除原生通知动作，替换为 OpenClaw 事件动作

## 最小恢复序列

```bash
mcporter list server ha-mcp --schema
mcporter call server.ha_config_list_areas
mcporter call server.ha_get_overview detail_level:minimal
```
