# 摄像头指南

用于摄像头实体搜索、主/子码流选择和当前帧获取。

## 关键事实

- 媒体入口只认 `camera.*` 实体。
- `binary_sensor.*` 只表示检测状态，不承载图像或视频字节流。
- 当前项目里已确认的两个摄像头实体：
  - `camera.tp_ipc_mainstream`：高清主码流
  - `camera.tp_ipc_minorstream`：低码率预览
- `camera.tp_ipc_substream` 不存在，不要编造或假设这个实体。

## 凭证来源

当前帧脚本不保存 HA 凭证。它按以下优先级读取宿主配置：

1. 环境变量：
   - `HOMEASSISTANT_URL`
   - `HOMEASSISTANT_TOKEN`
2. `ha-mcp` 配置：
   - 默认读取 `openclaw/config/mcporter.json`
   - 读取 `mcpServers.<server>.env.HOMEASSISTANT_URL`
   - 读取 `mcpServers.<server>.env.HOMEASSISTANT_TOKEN`
3. OpenClaw 插件配置：
   - 默认读取 `~/.openclaw/openclaw.json`
   - 读取 `plugins.entries.ha-bridge.config.haWsUrl`
   - 读取 `plugins.entries.ha-bridge.config.haToken`
   - `haWsUrl` 会被转换成对应的 HTTP 基地址

## 选择规则

- 用户要求普通预览、看一下现在画面：
  - 默认选 `camera.tp_ipc_minorstream`
- 用户要求高清、看细节、主码流：
  - 选 `camera.tp_ipc_mainstream`
- 用户只给房间名和设备名时：
  - 先 `ha_search_entities`
  - 优先匹配 `camera.*`

## 当前帧流程

1. 搜索摄像头实体：
```bash
mcporter call server.ha_search_entities query:'摄像头' domain_filter:camera
```
2. 若用户未指定高清，默认使用低码率预览：
```bash
python3 scripts/get_camera_frame.py --entity-id camera.tp_ipc_minorstream
```
3. 若用户要求高清：
```bash
python3 scripts/get_camera_frame.py --entity-id camera.tp_ipc_mainstream
```

## 已知限制

- `ha_get_camera_image` 在当前环境下不可靠，已出现 `HTTP 500`。
- 脚本会优先复用现有 HA 配置并自行获取当前帧。
- 若宿主环境缺少 `ffmpeg`，脚本会明确报错，不静默失败。

## 面向用户的表达

- 可以说“我用客厅摄像头的预览流给你取了一张当前帧”
- 不要说“我去读了 token”或展示配置文件路径
- 不要把 `binary_sensor` 说成图像来源
