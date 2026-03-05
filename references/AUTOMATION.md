# 自动化指南

用于创建、更新、读取和删除 Home Assistant 自动化。

## 关键工具事实

- 当前服务不支持 `ha_automation_create`。
- 创建和更新自动化统一使用 `ha_config_set_automation`。

## 工具清单

- 读取自动化：`ha_config_get_automation`
- 创建/更新自动化：`ha_config_set_automation`
- 删除自动化：`ha_config_remove_automation`

## 必须遵循的创建流程

1. 收到请求后第一步先用 `ha_search_entities` 搜索相关实体，不先输出计划说明。
2. 匹配处理规则：
   - 无歧义（唯一且明显匹配）时，可直接选中该实体并继续创建。
   - 有歧义时，先选一个最可能的候选（基于房间名/设备名语义），再用自然语言设备名（`friendly_name + 房间名`）让用户确认后写入。
3. 组装自动化配置。
4. 调用 `ha_config_set_automation` 写入。
5. 调用 `ha_config_get_automation` 回读验证。
6. 最后向用户周知本次采用的实体匹配结果与已创建动作（用自然语言设备名，不暴露技术 ID）。

## 标准交互示例

### 用户输入

> 当感应到有人的时候使用音箱播放"欢迎你"，打开开关，然后再通知我

### 正确做法

第一步：搜索实体（调用工具，不要输出任何内容）

- 搜索人体传感器
- 搜索音箱/媒体播放器
- 搜索开关/插座
- 对音箱实体调用 `ha_get_device` 获取 `device_id`（播报需要 `device_id`）

第二步：向用户确认匹配（有歧义时）

> 我准备为你创建自动化：
>
> 当客厅的人体传感器检测到有人时，用客厅小米音箱 Pro 播放"欢迎你"，打开客厅的米家插座3，并通知你。
>
> 你家有多个音箱，我默认用客厅那台，可以吗？确认后我就帮你创建。

第三步：用户确认后，生成正确的自动化 YAML 并写入

- 若匹配无歧义，可直接创建，但创建完成后仍需周知用户本次匹配与执行结果。

## “通知用户”与“设备播报”必须严格区分

- 通知用户（用户说“通知我/提醒我/告诉我”）：
  - 使用 OpenClaw 回调事件（默认 `notify_openclaw_agent`，特殊语义用 `notify_openclaw_direct`）。
  - 不使用 `notify.notify`、`notify.feishu`、`notify.mobile_app_xxx` 等 HA 原生通知服务。
  - 不使用 `nanobot_notify`（本 skill 为 OpenClaw 版本）。

- 设备播报（用户说“用音箱播放/播报”）：
  - 小米音箱使用 `notify.send_message`，并传 `target.device_id` 与消息内容。
  - 不使用 `tts.speak`。
  - 先搜索音箱实体，再用 `ha_get_device` 获取 `device_id`。

## OpenClaw 回调事件策略

- 默认事件：`notify_openclaw_agent`（V2）。
- 仅当用户要求“原文不改写/一字不差”或明确要求 V1 时，使用 `notify_openclaw_direct`（V1）。
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

## 创建示例 A（默认仅 V2）

YAML 示例：

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

`mcporter` 命令（已归一化为 `trigger`/`action`）：

```bash
mcporter call server.ha_config_set_automation config:'{"alias":"插座开启欢迎播报","description":"插座打开时触发 OpenClaw V2 欢迎提醒","mode":"single","trigger":[{"platform":"state","entity_id":"switch.cuco_cn_2028625295_v3_on_p_2_1","to":"on"}],"action":[{"event":"notify_openclaw_agent","event_data":{"message":"主人已回家，请生成一句更自然的欢迎提醒（V2）","source":"ha_automation","automation":"插座开启欢迎播报"}}]}'
```

## 创建示例 B（原文不改写，仅 V1）

YAML 示例：

```yaml
alias: 插座开启原文播报
description: 插座打开时触发 OpenClaw V1 原文通知
triggers:
  - trigger: state
    entity_id: switch.cuco_cn_2028625295_v3_on_p_2_1
    to: "on"
actions:
  - event: notify_openclaw_direct
    event_data:
      message: 欢迎回家，祝你生活愉快（V1）
      source: ha_automation
      automation: 插座开启原文播报
mode: single
```

`mcporter` 命令：

```bash
mcporter call server.ha_config_set_automation config:'{"alias":"插座开启原文播报","description":"插座打开时触发 OpenClaw V1 原文通知","mode":"single","trigger":[{"platform":"state","entity_id":"switch.cuco_cn_2028625295_v3_on_p_2_1","to":"on"}],"action":[{"event":"notify_openclaw_direct","event_data":{"message":"欢迎回家，祝你生活愉快（V1）","source":"ha_automation","automation":"插座开启原文播报"}}]}'
```

## 创建示例 C（显式要求 V1 + V2 兼容）

YAML 示例：

```yaml
alias: 插座开启欢迎播报
description: 插座打开时通过小米音箱播报，并触发 OpenClaw V1/V2
triggers:
  - trigger: state
    entity_id: switch.cuco_cn_2028625295_v3_on_p_2_1
    to: "on"
actions:
  - event: notify_openclaw_direct
    event_data:
      message: 欢迎回家，祝你生活愉快（V1）
      source: ha_automation
      automation: 插座开启欢迎播报
  - event: notify_openclaw_agent
    event_data:
      message: 主人已回家，请生成一句更自然的欢迎提醒（V2）
      source: ha_automation
      automation: 插座开启欢迎播报
mode: single
```

`mcporter` 命令：

```bash
mcporter call server.ha_config_set_automation config:'{"alias":"插座开启欢迎播报","description":"插座打开时通过小米音箱播报，并触发 OpenClaw V1/V2","mode":"single","trigger":[{"platform":"state","entity_id":"switch.cuco_cn_2028625295_v3_on_p_2_1","to":"on"}],"action":[{"event":"notify_openclaw_direct","event_data":{"message":"欢迎回家，祝你生活愉快（V1）","source":"ha_automation","automation":"插座开启欢迎播报"}},{"event":"notify_openclaw_agent","event_data":{"message":"主人已回家，请生成一句更自然的欢迎提醒（V2）","source":"ha_automation","automation":"插座开启欢迎播报"}}]}'
```

## 更新示例

传入 `identifier` 和新 `config`：

```bash
mcporter call server.ha_config_set_automation identifier:automation.welcome_message config:'{"alias":"Welcome Message","trigger":[...],"action":[...]}'
```

## 删除示例

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

## 面向用户的输出规范

- 只使用房间名/设备名等自然语言描述。
- 禁止展示 `entity_id`、`media_player.xxx`、`switch.xxx`、`automation.xxx` 等技术标识。
