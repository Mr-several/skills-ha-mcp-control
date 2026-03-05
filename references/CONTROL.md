# 控制指南

用于设备开关、参数设置和批量控制。

## 控制流程（强制）

1. 收到控制请求后，第一步先调用 `ha_search_entities` 搜索目标实体，不先输出计划说明。
2. 匹配判定：
   - 无歧义（唯一且明显匹配）：直接执行控制。
   - 有歧义：先选一个最可能候选，并向用户确认后再执行。
3. 执行控制后，调用 `ha_get_state` 验证结果。
4. 最后向用户周知：本次选中的设备（自然语言名称）和执行结果。

### 关闭插座标准流程

- 搜索插座/开关实体（如 `query:'插座'` 或 `domain_filter:switch`）。
- 若无歧义，直接 `switch.turn_off`。
- 若有歧义，给出你选中的默认候选并让用户确认。
- 执行后回读状态并反馈。

## 主要工具

- `ha_call_service`：首选，显式调用 HA 服务
- `ha_get_device`：获取设备详情（小米音箱播报必需）
- `ha_bulk_control`：多实体批量控制
- `ha_list_services`：先查看可调用服务定义

## 常用命令

- 开灯：
```bash
mcporter call server.ha_call_service domain:light service:turn_on data:'{"entity_id":"light.living_room"}'
```

- 关开关：
```bash
mcporter call server.ha_call_service domain:switch service:turn_off data:'{"entity_id":"switch.coffee_plug"}'
```

- 设置空调温度：
```bash
mcporter call server.ha_call_service domain:climate service:set_temperature data:'{"entity_id":"climate.bedroom_ac","temperature":24}'
```

## 小米音箱播报（硬规则）

- 不要对小米音箱使用 `tts.speak`。
- 必须使用 `notify.send_message`，并传 `target.device_id`。
- 必须先通过 `ha_get_device entity_id:<speaker_entity_id>` 获取 `device_id`。
- 本段仅用于“设备播报”，不用于“通知用户”。

流程：

1. 搜索音箱实体：
```bash
mcporter call server.ha_search_entities query:'小米音箱' domain_filter:media_player
```
2. 解析 `device_id`：
```bash
mcporter call server.ha_get_device entity_id:media_player.xiaomi_cn_2085725100_oh2p
```
3. 执行播报：
```bash
mcporter call server.ha_call_service domain:notify service:send_message data:'{"message":"欢迎你","target":{"device_id":"e0e28fxxxxxxxx"}}'
```

## 验证

每次控制后都要验证状态：
```bash
mcporter call server.ha_get_state entity_id:light.living_room
```
