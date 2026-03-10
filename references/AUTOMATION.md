# 自动化指南

用于创建、更新、读取和删除 Home Assistant 自动化。

当触发条件涉及识别人的具体行为或动作（如"检测到玩手机""看到在看电脑/电视""发现躺在床上""有人摔倒""孩子哭了"），这类场景不能用普通传感器实现，必须加载 `references/LLM_VISION.md` 并按其流程创建视觉自动化。

## 工具清单

- 创建/更新自动化：`ha_config_set_automation`
- 读取自动化：`ha_config_get_automation`
- 删除自动化：`ha_config_remove_automation`

注意：当前服务不支持 `ha_automation_create` 和 `ha_create_automation`，这些名称不存在。

## 禁止模式

### 禁止 1：禁止使用 `action: event.fire` 发送 OpenClaw 通知

错误写法：

```yaml
# 错误！禁止这样写！
actions:
  - data:
      event_type: notify_openclaw_agent
      event_data:
        message: 摄像头检测到有人活动
        source: ha_automation
        automation: xxx
    action: event.fire
```

正确写法：

```yaml
actions:
  - event: notify_openclaw_agent
    event_data:
      message: 摄像头检测到有人活动
      source: ha_automation
      automation: xxx
```

### 禁止 2：禁止对小米音箱使用错误的播报方式

小米音箱播报**唯一正确写法**是 `notify.send_message` + `target.device_id`：

```yaml
actions:
  - action: notify.send_message
    target:
      device_id: e0e28f9f97a057c47067863a7f0e5408
    data:
      message: 欢迎回家
```

以下写法全部禁止：

- `action: notify.xiaomi_cn_xxx_play_text_xxx`（设备专属 notify 服务，禁止使用）
- `action: media_player.play_media` + `media_content_type: announce`（禁止使用）
- `action: tts.speak`（禁止使用）

必须先通过 `ha_get_device` 获取音箱的 `device_id`，不要使用 `entity_id` 代替。完整规则见 `references/CONTROL.md` 的"小米音箱播报"章节。

### 禁止 3：禁止使用 HA 原生通知服务通知用户

禁止在自动化中使用 `notify.notify`、`notify.mobile_app_xxx`、`notify.feishu`、`persistent_notification.create` 等 HA 原生通知服务。

所有面向用户的通知必须走 OpenClaw 事件。唯一例外：用户明确指定了某个 HA 原生通知渠道。

## HA 自动化动作类型

### 服务调用（控制设备）

```yaml
- action: notify.send_message
  target:
    device_id: e0e28f9f97a057c47067863a7f0e5408
  data:
    message: 欢迎回家
```

### 事件触发（通知 OpenClaw）

```yaml
- event: notify_openclaw_agent
  event_data:
    message: 摄像头检测到有人活动
    source: ha_automation
    automation: xxx
```

关键区别：服务调用用 `action:`，事件触发用 `event:`，二者不可互换。

## 创建流程

1. 收到请求后第一步先用 `ha_search_entities` 搜索相关实体，不先输出计划说明。
   - 触发源搜索至少一次：`query:'摄像头'` 或 `query:'人体'`，并结合 `domain_filter:binary_sensor,camera`。
   - 音箱搜索至少一次：`query:'音箱'`，并结合 `domain_filter:media_player`。
   - 对音箱实体调用 `ha_get_device` 获取 `device_id`（播报必须使用 `notify.send_message` + `target.device_id`，禁止使用设备专属 notify 服务）。
2. 匹配处理规则：
   - 无歧义（唯一且明显匹配）时，可直接选中该实体并继续创建。
   - 有歧义时，先选一个最可能的候选（基于房间名/设备名语义），再用自然语言设备名让用户确认后写入。
   - 若语义信息本身缺失，最多补问 1 个自然语言问题，不得索要任何 ID。
3. 组装自动化配置。
4. 调用 `ha_config_set_automation` 写入。
5. 调用 `ha_config_get_automation` 回读验证。
6. 最后向用户周知本次采用的实体匹配结果与已创建动作（用自然语言设备名，不暴露技术 ID）。

## 标准交互示例

用户输入：

> 当感应到有人的时候使用音箱播放"欢迎你"，打开开关，然后再通知我

正确做法：

第一步：搜索实体（调用工具，不要输出任何内容）

- 搜索人体传感器
- 搜索音箱/媒体播放器
- 搜索开关/插座
- 对音箱实体调用 `ha_get_device` 获取 `device_id`

第二步：若有歧义，先给出默认候选并向用户确认

> 我准备为你创建自动化：
>
> 当客厅的人体传感器检测到有人时，用客厅小米音箱 Pro 播放"欢迎你"，打开客厅的米家插座3，并通知你。
>
> 你家有多个音箱，我默认用客厅那台，可以吗？确认后我就帮你创建。

第三步：用户确认后，生成正确的自动化 YAML 并写入

- 若匹配无歧义，可直接创建，但创建完成后仍需周知用户本次匹配与执行结果。

## OpenClaw 回调事件策略

- 默认事件：`notify_openclaw_agent`（V2）。
- 仅当用户要求"原文不改写/一字不差"或明确要求 V1 时，使用 `notify_openclaw_direct`（V1）。
- 仅当用户明确要求 V1+V2 兼容时，才同时创建双事件。
- 双事件时顺序固定：`notify_openclaw_direct` -> `notify_openclaw_agent`。
- 事件数据最小字段：
  - `event_data.message`
  - `event_data.source`（默认 `ha_automation`）
  - `event_data.automation`
- 自动纠正拼写：`notify_openclaw_agen` -> `notify_openclaw_agent`。

## 字段归一化规则

- 用户示例可使用 YAML 的 `triggers` / `actions`。
- 实际调用 `ha_config_set_automation` 时，`config` 必须归一化为 `trigger` / `action`。
- `event.*` 实体触发器必须使用 state trigger（`trigger: state` 或 `platform: state`），不要使用 event platform。

## 冷却时间 / 防频繁触发

用户要求"X 分钟内只触发一次"时，使用 `mode: single` + 末尾 `delay:` 实现：

```yaml
actions:
  - action: notify.send_message
    target:
      device_id: e0e28f9f97a057c47067863a7f0e5408
    data:
      message: 欢迎回家
  - event: notify_openclaw_agent
    event_data:
      message: 摄像头检测到有人活动
      source: ha_automation
      automation: xxx
  - delay:
      minutes: 5
mode: single
```

如果用户没有要求防频繁触发，不需要加 `delay`，仅保留 `mode: single` 即可。

## 创建示例

### 完整示例（默认 V2）

YAML：

```yaml
alias: 插座开启欢迎播报
description: 插座打开时触发 OpenClaw V2 欢迎提醒
triggers:
  - trigger: state
    entity_id: switch.cuco_cn_2028625295_v3_on_p_2_1
    to: "on"
actions:
  - event: notify_openclaw_agent
    event_data:
      message: 主人已回家，请生成一句更自然的欢迎提醒（V2）
      source: ha_automation
      automation: 插座开启欢迎播报
mode: single
```

mcporter 命令（已归一化为 `trigger`/`action`）：

```bash
mcporter call server.ha_config_set_automation config:'{"alias":"插座开启欢迎播报","description":"插座打开时触发 OpenClaw V2 欢迎提醒","mode":"single","trigger":[{"platform":"state","entity_id":"switch.cuco_cn_2028625295_v3_on_p_2_1","to":"on"}],"action":[{"event":"notify_openclaw_agent","event_data":{"message":"主人已回家，请生成一句更自然的欢迎提醒（V2）","source":"ha_automation","automation":"插座开启欢迎播报"}}]}'
```

### 事件类型变体

上面示例使用 V2（默认）。其他变体只需替换 actions 中的事件部分：

| 场景 | 事件名 | message 示例 |
|------|--------|-------------|
| 默认（AI 润色后通知） | `notify_openclaw_agent` | 主人已回家，请生成一句更自然的欢迎提醒 |
| 原文不改写 | `notify_openclaw_direct` | 欢迎回家，祝你生活愉快 |
| V1+V2 兼容 | 先 `notify_openclaw_direct` 再 `notify_openclaw_agent` | 两个事件各自的 message |

## 更新自动化

传入 `identifier` 和新 `config`：

```bash
mcporter call server.ha_config_set_automation identifier:automation.welcome_message config:'{"alias":"Welcome Message","trigger":[...],"action":[...]}'
```

## 删除自动化

```bash
mcporter call server.ha_config_remove_automation identifier:automation.welcome_message
```

## 安全建议

执行破坏性改动前先备份：

```bash
mcporter call server.ha_backup_create name:Before_Automation_Change
```

## 写后验证

创建或更新后：

```bash
mcporter call server.ha_config_get_automation identifier:automation.welcome_message
```

确认事件类型和 `event_data` 字段正确。

## 完成态输出门槛

- 若未执行 `ha_config_set_automation`，禁止输出"已创建""正在创建""已生效"。
- 若未执行或未通过 `ha_config_get_automation` 回读，禁止输出"创建成功"。
- 上述任一步失败时，必须明确写出"尚未创建成功"，并给出下一步动作。

## 失败处理

- 若出现 `Unknown tool`（尤其是 `ha_create_automation` / `ha_automation_create`）：
  1. 重新执行 `mcporter list server ha-mcp --schema`
  2. 改用 `ha_config_set_automation` 重试
  3. 仅在写入和回读验证都成功后才可回复"创建成功"
- 若写入失败（鉴权、连接、配置错误），必须明确告知"尚未创建成功"，并给出可直接粘贴的 YAML 兜底。
