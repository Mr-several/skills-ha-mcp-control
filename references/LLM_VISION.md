# 视觉自动化指南

用于在自动化中调用 LLM Vision 服务实现摄像头画面感知、人体姿势/手势识别等场景。

LLM Vision 不是常驻后台服务，它由自动化触发后抓取图片或短时视频帧，发给大模型分析，再根据返回结果执行后续动作。真正决定调用频率的是自动化的触发器和冷却设计，不是 LLM Vision 本身。

## 可用服务及优先级

1. `llmvision.image_analyzer` — 单张图够用时优先使用
2. `llmvision.stream_analyzer` — 需要看短时间动作时使用（当前 TP 摄像头场景推荐）
3. `llmvision.video_analyzer` — 已有视频文件时使用

## 推荐参数

为节省 token，建议使用以下参数：

- `duration: 4`
- `max_frames: 2`
- `target_width: 960`

优先使用次码流，次码流更轻、更容易抓帧成功、更适合分析型任务。具体摄像头实体需通过 `ha_search_entities` 搜索确认。

## 自动化中的 provider 配置

自动化里调用 LLM Vision 时，provider 字段必须填 config entry id，不能填显示名称。

- 错误：`provider: Custom OpenAI`
- 正确：`provider: 01KKB4QRM40H87FB1Q7JB7YK49`

填错会报 `Provider config not found for entry_id`。

## 结构化返回

推荐让模型直接返回 JSON，不要返回自然语言再做关键词匹配。

服务调用参数示例：

```yaml
response_format: json
structure: >
  {
    "type": "object",
    "properties": {
      "is_playing_phone": {"type": "boolean"},
      "summary": {"type": "string"}
    },
    "required": ["is_playing_phone", "summary"],
    "additionalProperties": false
  }
```

然后在自动化中用模板条件判断：

```yaml
{{ vision_result.structured_response is defined and vision_result.structured_response.is_playing_phone == true }}
```

## 自动化设计模式

### 方案 A：简单触发

适合"有人出现时分析一次"的场景。

流程：触发器传感器从 off -> on → 调用 `llmvision.stream_analyzer` → 模型返回结果 → 命中后播报和通知。

创建前需通过 `ha_search_entities` 搜索摄像头关联的传感器，按以下优先级选择触发器：

1. 人体检测传感器（如 `person_detection`）— 最精准，优先使用
2. 运动检测传感器（如 `motion_detection`、`cell_motion_detection`）— 人体检测不可用时的替代
3. 其他可用的 `binary_sensor`（如物体检测）— 视具体摄像头能力选择
4. 如果该摄像头没有任何关联传感器，降级为定时轮询：使用 `time_pattern` 触发器（如每 5 分钟触发一次），token 消耗较高，仅作兜底

不同摄像头的传感器命名差异较大，不要假设固定名称，始终搜索后再决定。

优点：简单、token 消耗低（使用传感器触发时）。
缺点：人一直在原地不动时，传感器不一定会反复触发；定时轮询模式下 token 消耗较高。

### 方案 B：高频检测 + 低频复查

适合"持续坐在电脑前 / 持续玩手机"等需要持续监测的场景。

配合 `input_boolean` 实现冷却控制，需要两条自动化配合：

- `<业务名>｜检测` — 主检测自动化
- `<业务名>｜复位` — 冷却复位自动化

逻辑：

1. 未命中前，每 30 秒检查一次
2. 命中后，把冷却开关设为 on
3. 冷却期间改为每 5 分钟检查一次
4. 当触发器传感器连续 2 分钟为 off（或定时轮询模式下连续 N 次未命中），自动清除冷却，恢复高频检查

触发器传感器的选择同方案 A 的优先级规则。如果使用定时轮询作为触发器，复位条件需改为"连续 N 次分析未命中目标行为"。

这种设计比单纯用 `delay` 更容易理解和维护。

## 让 OpenClaw 带上当前图像

不在事件里传图片二进制，而是：

1. 在 LLM Vision 调用中打开 `expose_images: true`
2. 让 LLM Vision 返回 `key_frame`
3. 在 `notify_openclaw_agent` 的 message 里把本地路径告诉 OpenClaw

```yaml
message: >
  请立即通知我，并把当前抓拍图像作为图片发送给我，不要只发路径文本。
  图像本地路径：{{ vision_result.key_frame if vision_result.key_frame is defined else "" }}。
```

注意：依赖 OpenClaw 侧正确读取该本地路径并转成图片消息。如果抓帧失败，退化为纯文字通知。

## 踩坑记录

### 摄像头 RTSP 流不稳定导致 LLM Vision 完全失败

常见错误：`Couldn't fetch frame (status code: 500)`、`No cameras available`、`dial tcp ... i/o timeout`。

问题不在模型，而是 HA 无法从摄像头取到帧。排查方向：

1. 摄像头 RTSP / ONVIF 是否开启
2. 摄像头 IP 是否变化
3. 554 端口是否可达
4. 是否优先使用次码流
5. 摄像头是否需要重启

### 传感器不是持续触发

摄像头关联的传感器（人体检测、运动检测等）状态切到 on 时触发一次，不是"人一直在就不断触发"。要实现持续监测某个行为，需要配合定时轮询（见方案 B）。如果摄像头没有任何关联传感器，直接使用定时轮询作为触发器。

## 推荐落地流程

新增一条视觉自动化时，按以下顺序做：

1. 确认 LLM Vision 页面模型 provider 已连通
2. 找到自动化要用的真实 provider entry_id
3. 通过 `ha_search_entities` 搜索确认摄像头实体和触发器传感器（按优先级：人体检测 > 运动检测 > 其他传感器 > 定时轮询兜底）
4. 先用次码流，小参数版本（duration:4, max_frames:2, target_width:960）
5. 让模型返回 JSON
6. 用模板条件判断命中
7. 音箱播报和 OpenClaw 通知分别配置（规则见 `references/CONTROL.md`）
8. 根据场景选择设计模式（方案 A 或 B）
9. 观察 HA 日志，重点看触发器是否触发、LLM Vision 是否抓到帧、摄像头流是否报错

## 命名规范

同一组业务自动化按统一前缀命名：

- `玩手机提醒｜检测`
- `玩手机提醒｜复位`
- `看电脑提醒｜检测`
- `看电脑提醒｜复位`
