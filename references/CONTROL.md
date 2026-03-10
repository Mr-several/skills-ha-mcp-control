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

- 搜索插座或开关实体（如 `query:'插座'` 或 `domain_filter:switch`）。
- 若无歧义，直接 `switch.turn_off`。
- 若有歧义，给出你选中的默认候选并让用户确认。
- 执行后回读状态并反馈。

## 主要工具

- `ha_call_service`：首选，显式调用 HA 服务
- `ha_get_device`：获取设备详情（小米音箱播报必需）
- `ha_bulk_control`：多实体批量控制
- `ha_list_services`：先查看可调用服务定义

## 控制方式优先级（硬规则）

1. 先检查目标设备是否有原生控制服务（先 `ha_list_services`，再按设备 domain 调用）。
2. 若存在原生控制服务，必须优先走原生控制，不先用文本通知或播报接口兜底。
3. 对音箱类设备：
   - "播放音乐/暂停/下一首/调音量"优先 `media_player.*`。
   - `notify.send_message` 只用于播报文本，不用于播放歌曲。

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

## 小米音箱播报（硬规则，必须严格遵守）

**唯一正确方式：`notify.send_message` + `target.device_id`。**

以下方式全部禁止，无论在实时控制还是自动化中：

- 禁止使用设备专属 notify 服务（如 `notify.xiaomi_cn_xxx_play_text_xxx`）
- 禁止使用 `tts.speak`
- 禁止使用 `media_player.play_media` + `media_content_type: announce`

必须先通过 `ha_get_device entity_id:<speaker_entity_id>` 获取 `device_id`，然后用 `notify.send_message` + `target.device_id` 播报。本段仅用于"设备播报"，不用于"通知用户"，也不用于"播放歌曲/播放音乐"。

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

### 自动化中的播报动作格式

在自动化 YAML 的 `actions` 中使用以下格式：

```yaml
- action: notify.send_message
  target:
    device_id: e0e28f9f97a057c47067863a7f0e5408
  data:
    message: 欢迎回家
```

对应 mcporter JSON：

```json
{"action":"notify.send_message","target":{"device_id":"e0e28f9f97a057c47067863a7f0e5408"},"data":{"message":"欢迎回家"}}
```

禁止在自动化中使用以下写法播报文字：

```yaml
# 错误！禁止这样写！
- action: media_player.play_media
  target:
    entity_id: media_player.xiaomi_cn_2085725100_oh2p
  data:
    media:
      media_content_id: 欢迎回家
      media_content_type: announce
```

```yaml
# 错误！禁止这样写！
- data:
    message: 欢迎回家
  action: notify.xiaomi_cn_2085725100_oh2p_play_text_a_7_3
```

## 小米音箱播放音乐（硬规则）

- 优先用 `media_player` 的原生媒体控制。
- 用户说"播放音乐/放歌"时：
  - 有明确媒体内容（歌曲名、URL、歌单）优先 `media_player.play_media`。
  - 无明确媒体内容但设备有历史队列时，使用 `media_player.media_play` 恢复播放。
- 不要用 `notify.send_message` 承载"播放音乐"意图。

示例：

```bash
mcporter call server.ha_call_service domain:media_player service:media_play data:'{"entity_id":"media_player.xiaomi_speaker"}'
```

## 验证

每次控制后都要验证状态：
```bash
mcporter call server.ha_get_state entity_id:light.living_room
```

## 面向用户输出约束

- 禁止向用户索要 `entity_id`、`device_id`、服务名等技术参数。
- 禁止在回复中暴露任何实体 ID 或自动化 ID。
