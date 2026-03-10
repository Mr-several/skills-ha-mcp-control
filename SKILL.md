---
name: openclaw-ha-mcp
description: "智能家居设备控制、状态查询与自动化管理。Use when: (1) 用户提到家里的设备（灯、开关、插座、窗帘、空调、音箱、传感器等）, (2) 询问家中状态（温度、湿度、谁在家、灯开着吗）, (3) 查看摄像头画面或截图, (4) 要求执行场景或脚本, (5) 设置定时、联动、自动化规则, (6) 提到通知/提醒/播报等家庭联动需求, (7) 要求识别特定行为并触发动作（检测到玩手机、看到在看电脑/电视、发现躺在床上/沙发上、有人摔倒、孩子哭了等）。NOT for: 未接入智能家居系统的设备, 网络设备管理（路由器/NAS）, 系统安装或 OS 级运维。"
---

# Home Assistant 智能家居控制

通过 `mcporter + ha-mcp` 在安全、可验证、可回溯的前提下执行 Home Assistant 操作。

## When to Use

✅ **USE this skill when:**

- 用户提到家里的设备（"开灯""关空调""拉窗帘""我家插座关了吗"）
- 用户询问家中环境或设备状态（"现在几度""湿度多少""灯开着吗"）
- 用户要求查看摄像头画面（"看一下家里""给我截个图"）
- 用户要求执行场景或脚本（"回家模式""睡眠模式"）
- 用户要求设置定时、联动、自动化规则（"有人回家就开灯""每天7点开窗帘"）
- 用户提到通知、提醒、播报等家庭联动需求
- 用户要求通过摄像头识别特定行为并触发动作（"检测到玩手机就提醒""看到在看电脑/电视就通知我""发现躺在床上/沙发上就提醒""有人摔倒就报警""孩子哭了就通知"）

## When NOT to Use

❌ **DON'T use this skill when:**

- 未接入智能家居系统的设备 → 使用对应平台的工具
- 网络设备管理（路由器、NAS、交换机） → 使用网络管理工具
- 系统安装、OS 升级、Docker 部署 → 使用系统运维技能
- 纯知识问答（"什么是 Zigbee"） → 直接回答，不需要调用工具

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

## 凭证与连接

本 skill 不管理 Home Assistant 凭证，复用宿主已有配置：

- 优先使用 `openclaw/config/mcporter.json` 中的 `HOMEASSISTANT_URL` / `HOMEASSISTANT_TOKEN`
- 若 `ha-mcp` 配置不可用，再读取 OpenClaw 配置 `plugins.entries.ha-bridge.config` 下的 `haWsUrl` / `haToken`

## 意图路由

| 用户意图 | 加载文档 |
|---------|---------|
| 查询/盘点/状态读取 | `references/QUERY.md`（实体搜索、状态读取、全量盘点命令） |
| 设备/服务控制 | `references/CONTROL.md`（控制流程、服务调用优先级、音箱播报/音乐播放、验证） |
| 摄像头当前帧 | `references/CAMERA.md`（实体选择规则、主/子码流、脚本调用） |
| 自动化创建/更新/删除 | `references/AUTOMATION.md`（工具映射、创建流程、回调事件策略、禁止模式、示例） |
| 识别特定行为并触发（检测到玩手机、看到看电脑/电视、发现躺床上、有人摔倒等） | `references/LLM_VISION.md` + `references/AUTOMATION.md`（视觉自动化流程、LLM Vision 服务调用、设计模式、参数配置） |
| 报错/连接/鉴权问题 | `references/TROUBLESHOOTING.md`（连接失败、Unknown tool、格式错误修复） |
| 工具参数速查 | `references/TOOLS.md`（92个 ha-mcp 工具的完整参数表） |

## 接管范围

- 只要用户意图是智能家居查询或控制（例如"开灯""关插座""查温度"），默认由本 skill 接管，即使用户没有显式说"HA"。
- 用户说"通过 HA 操作"时，必须立即按本 skill 执行工具调用，不要退回到通用问答流程。
- 不要求用户提供 `entity_id`。必须先自行搜索实体并匹配。
- 不向用户询问"是否已授权平台"这类前置问题；先按工具链执行搜索与匹配，必要时再反馈具体失败原因。

## 音箱播报硬规则

**所有小米音箱播报必须使用 `notify.send_message` + `target.device_id`。** 禁止使用设备专属 notify 服务（如 `notify.xiaomi_cn_xxx_play_text_xxx`）、`tts.speak`、`media_player.play_media` + `announce`。必须先通过 `ha_get_device` 获取 `device_id`。详见 `references/CONTROL.md` 的"小米音箱播报"章节。

## 交互规则

- 当用户的触发条件涉及识别特定行为（如"检测到玩手机""看到在看电脑""发现躺在床上""有人摔倒""孩子哭了"等），这类行为不能通过普通传感器直接检测，必须先加载 `references/LLM_VISION.md`，按其流程创建视觉自动化，不要尝试寻找对应的行为传感器。
- 用户通常不知道 `entity_id`，只会给房间名和设备名。必须先自行搜索实体并匹配。
- 收到涉及设备或自动化的请求后，第一步先调用 `ha_search_entities`，不要先输出计划说明。
- 收到"看摄像头/看当前画面/拿当前帧"请求时，先搜索 `camera.*` 实体，再决定使用主码流还是低码率预览。
- 搜索完成后，若匹配无歧义可直接选中并继续；若有歧义，先选一个最可能候选，再用 `friendly_name + 房间名` 让用户确认。
- 回复中不要出现 `entity_id`、`media_player.xxx`、`switch.xxx`、`automation.xxx` 等技术标识符。
- 自动化执行顺序：搜索 -> 判断是否歧义 ->（有歧义则确认）-> 写入 -> 回读验证 -> 周知用户最终匹配与执行结果。
- 设备控制执行顺序：搜索 -> 判断是否歧义 ->（无歧义直接执行 / 有歧义确认）-> 执行 -> 验证 -> 周知用户结果。
- 当前帧执行顺序：搜索 `camera.*` -> 选择主/子码流 -> 调用 `{baseDir}/scripts/get_camera_frame.py` -> 验证输出文件存在 -> 向用户返回结果。
- 回复保持简洁自然，不堆 emoji，不加无请求的优化建议。
- 不要暴露内部推理或调试痕迹（例如 `Intent:`、`retry`、`fix config`、`JSON encoding`）。
- 工具调用返回 `Unknown tool` 时，必须先重新执行 `mcporter list server ha-mcp --schema`，再按映射工具重试。
- 若写入失败或环境不支持写操作，必须明确告知"尚未创建成功"，不能宣称已经完成。

## 全局调用格式

```bash
mcporter call server.<tool> key:value key2:value2
```
- 包含空格的参数要加引号：`name:'Living Room'`
- JSON 载荷统一使用单引号包裹。
- 只能传 `references/TOOLS.md` 定义过的参数。
- 高风险操作（删除、重置、门锁/安防/报警、水气阀门、大功率设备）必须先确认；普通灯/开关/插座开关在无歧义时可直接执行。
