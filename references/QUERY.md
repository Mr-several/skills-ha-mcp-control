# 查询指南

用于实体盘点、实体搜索和状态读取。

## 关键规则

- `ha_get_states` 仅支持按 `entity_ids` 批量查询，不支持通配符或“全部实体”。
- 需要全量实体盘点时使用 `ha_get_overview detail_level:full`。

## 常用命令

- 全量盘点快照：
```bash
mcporter call server.ha_get_overview detail_level:full
```

- 按域/类型搜索：
```bash
mcporter call server.ha_search_entities query:light limit:50
mcporter call server.ha_search_entities query:sensor limit:50
mcporter call server.ha_search_entities query:switch limit:50
```

- 读取单个实体状态：
```bash
mcporter call server.ha_get_state entity_id:light.living_room
```

- 批量读取指定实体状态：
```bash
mcporter call server.ha_get_states entity_ids:light.living_room,switch.ac_plug,sensor.temperature
```

## 推荐流程

1. `ha_get_overview detail_level:full`
2. 用 `ha_search_entities` 做二次筛选
3. 用 `ha_get_state` / `ha_get_states` 做精确核验
