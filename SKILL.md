---
name: openclaw-ha-mcp
description: 所有智能家居控制与自动化管理。通过 Home Assistant MCP 工具控制设备、执行场景脚本、创建/管理自动化规则、注入通知事件。
---

# OpenClaw 通过 ha-mcp 连接 Home Assistant

## 目标

在保证安全、可验证、可回溯的前提下，使用 `mcporter + ha-mcp` 执行 HA 操作，并尽量减少无关上下文。

本 skill 不管理 Home Assistant 凭证，也不要求用户在 skill 中额外配置 token。所有 HA 连接信息都应复用宿主已有配置：

- 优先使用 `openclaw/config/mcporter.json` 中的 `HOMEASSISTANT_URL` / `HOMEASSISTANT_TOKEN`
- 若 `ha-mcp` 配置不可用，再读取 OpenClaw 配置 `plugins.entries.ha-bridge.config` 下的 `haWsUrl` / `haToken`

当用户要求“获取摄像头当前帧”时，本 skill 应调用附带脚本 `scripts/get_camera_frame.py`，而不是要求用户手工提供 token。

## TRIGGER THIS SKILL WHEN

- 用户提到任何与智能家居、家庭设备、家庭自动化相关的内容
- 用户要求控制设备（灯、开关、插座、窗帘、传感器、音箱、空调等）
- 用户询问设备状态或传感器读数
- 用户要求查看摄像头当前画面、当前帧、截图、预览
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

## 自动化工具名硬映射（必须遵守）

- 自动化创建/更新唯一写入工具：`ha_config_set_automation`。
- 禁止调用不存在或历史别名：`ha_create_automation`、`ha_automation_create`。
- 读取与删除固定使用：`ha_config_get_automation`、`ha_config_remove_automation`。
- 任何写入结果都必须写后回读成功后，才可对用户宣称“已创建”或“已更新”。

## 意图路由（按需加载）

- 查询/盘点/状态读取：打开 `references/QUERY.md`
- 设备/服务控制：打开 `references/CONTROL.md`
- 摄像头实体、主/子码流、当前帧：打开 `references/CAMERA.md`
- 自动化创建/更新/删除：打开 `references/AUTOMATION.md`
- 报错/连接/鉴权/Supervisor 问题：打开 `references/TROUBLESHOOTING.md`
- 完整 92 个工具参数表：打开 `references/TOOLS.md`

## 接管范围（必须执行）

- 只要用户意图是智能家居查询或控制（例如“开灯”“关插座”“查温度”），默认由本 HA skill 接管，即使用户没有显式说“HA”。
- 用户说“通过 HA 操作”时，必须立即按本 skill 执行工具调用，不要退回到通用问答流程。
- 不要求用户提供 `entity_id`。必须先自行搜索实体并匹配。
- 不向用户询问“是否已授权平台”这类前置问题；先按工具链执行搜索与匹配，必要时再反馈具体失败原因。
- 用户要求查看摄像头时，媒体入口只认 `camera.*` 实体；`binary_sensor.*` 只能作为检测状态来源，不能作为图像来源。

## OpenClaw 自动化回调策略

- 自动化任务必须遵循 `references/AUTOMATION.md`。
- 自动化中的设备动作，必须复用 `references/CONTROL.md` 的原生控制优先规则。
- 自动化中的音箱播报必须使用 `notify.send_message` + `target.device_id`，禁止使用 `media_player.play_media` + `announce`。
- 默认回调事件使用 V2：`notify_openclaw_agent`。
- 仅当用户要求“原文不改写/一字不差”或明确要求 V1 时，使用 `notify_openclaw_direct`。
- 仅当用户明确要求 V1+V2 兼容时，才同时创建两个事件，顺序固定为 `notify_openclaw_direct` 后 `notify_openclaw_agent`。
- 面向用户的通知统一走 OpenClaw 事件，除非用户明确指定 HA 原生通知渠道。
- 通知事件在自动化中必须使用 HA 事件动作语法（`event:` 键 + `event_data:`），禁止使用 `action: event.fire`。
- 事件载荷必须包含 `event_data.message`、`event_data.source`、`event_data.automation`。
- `event_data.source` 默认值为 `ha_automation`。
- 自动纠正拼写错误：`notify_openclaw_agen` -> `notify_openclaw_agent`。

## 交互与执行硬规则

- 用户通常不知道 `entity_id`，只会给房间名和设备名。必须先自行搜索实体并匹配。
- 收到涉及设备或自动化的请求后，第一步先调用 `ha_search_entities`，不要先输出计划说明。
- 收到“看摄像头/看当前画面/拿当前帧”请求时，先搜索 `camera.*` 实体，再决定使用主码流还是低码率预览。
- 搜索完成后，若匹配无歧义可直接选中并继续；若有歧义，先选一个最可能候选，再用 `friendly_name + 房间名` 让用户确认。
- 回复中不要出现 `entity_id`、`media_player.xxx`、`switch.xxx`、`automation.xxx` 等技术标识符。
- 自动化执行顺序：搜索 -> 判断是否歧义 ->（有歧义则确认）-> 写入 -> 回读验证 -> 周知用户最终匹配与执行结果。
- 设备控制执行顺序：搜索 -> 判断是否歧义 ->（无歧义直接执行 / 有歧义确认）-> 执行 -> 验证 -> 周知用户结果。
- 当前帧执行顺序：搜索 `camera.*` -> 选择主/子码流 -> 调用 `scripts/get_camera_frame.py` -> 验证输出文件存在 -> 向用户返回结果。
- 回复保持简洁自然，不堆 emoji，不加无请求的优化建议。
- 不要暴露内部推理或调试痕迹（例如 `Intent:`、`retry`、`fix config`、`JSON encoding`）。
- 工具调用返回 `Unknown tool` 时，必须先重新执行 `mcporter list server ha-mcp --schema`，再按映射工具重试。
- 若写入失败或环境不支持写操作，必须明确告知“尚未创建成功”，不能宣称已经完成。
- `event.*` 实体触发必须使用 state trigger，不使用 event platform 或编造 `event_type`。
- 智能硬件控制先检查是否有设备原生控制服务；有原生控制时优先使用原生控制，不先走文本通知或播报接口。
- 对音箱类设备：播放/暂停/下一首/音量等媒体控制优先 `media_player.*`；`notify.send_message` 仅用于播报文字，不用于播放音乐。
- 禁止使用 `action: event.fire` 发送 OpenClaw 通知，必须使用 `event:` 键直接触发事件。
- 禁止对小米音箱使用 `media_player.play_media` + `media_content_type: announce` 播报文字。

## 自动化创建执行闸门（必须满足）

- 对“创建自动化”请求，禁止先提问；必须先执行最小工具链：
  1. `ha_search_entities`（触发源，优先 `binary_sensor`、`camera`）
  2. `ha_search_entities`（执行设备，按目标设备类型过滤）
  3. 对音箱实体调用 `ha_get_device` 获取 `device_id`（播报需要）
  4. `ha_config_set_automation`
  5. `ha_config_get_automation` 回读验证
- 仅在完成搜索后仍无法确定目标时，才允许补问 1 个自然语言问题。
- 只要写入或回读验证未成功，禁止输出“已创建”“已生效”这类完成态表述。

## 摄像头默认规则

- `camera.tp_ipc_mainstream`：用于外部实时主画面、高清截图。
- `camera.tp_ipc_minorstream`：用于低带宽预览、普通当前帧。
- 用户只说“看一下当前画面/给我截图”时，默认优先低码率预览。
- 用户明确要求“高清/看细节/主码流”时，使用 `camera.tp_ipc_mainstream`。
- 当前环境下 `ha_get_camera_image` 不可靠；当前帧优先通过 `scripts/get_camera_frame.py` 获取。

## 全局调用规则

- 调用格式：
```bash
mcporter call server.<tool> key:value key2:value2
```
- 包含空格的参数要加引号：`name:'Living Room'`
- JSON 载荷统一使用单引号包裹。
- 只能传 `references/TOOLS.md` 定义过的参数。
- 自动化请求必须先用 `ha_search_entities` 搜索实体，再按无歧义直接执行 / 有歧义确认的规则写入。
- 面向用户回复时，禁止输出技术标识（`entity_id`、`xxx.yyy` 实体 ID 等）。
- 高风险操作（删除、重置、门锁/安防/报警、水气阀门、大功率设备）必须先确认；普通灯/开关/插座开关在无歧义时可直接执行。
- 每次写操作后都要执行至少一次读操作进行验证。

## 当前帧脚本

- 脚本路径：`scripts/get_camera_frame.py`
- 示例：
```bash
python3 scripts/get_camera_frame.py --entity-id camera.tp_ipc_minorstream
python3 scripts/get_camera_frame.py --entity-id camera.tp_ipc_mainstream --output /tmp/main_frame.jpg
```
- 脚本只复用现有宿主配置，不新增 skill 私有 token 配置。
