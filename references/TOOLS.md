# ha-mcp Tools Reference
Total tools: 92
Generated from: `mcporter list server ha-mcp --json`

## How to Read
- `Required` = must provide when calling tool.
- `Default` = value used when omitted (if defined).
- Call pattern: `mcporter call server.<tool> key:value ...`

## 1. `ha_get_addon`
Get Home Assistant add-ons - list installed or available from store.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `source` | no | `string|null` | `null` | Add-on source: 'installed' (default) for currently installed add-ons, 'available' for add-ons in the store that can b... |
| `include_stats` | no | `boolean` | `False` | Include CPU/memory usage statistics (only for source='installed') |
| `repository` | no | `string|null` | `null` | Filter by repository slug, e.g., 'core', 'community' (only for source='available') |
| `query` | no | `string|null` | `null` | Search filter for add-on names/descriptions (only for source='available') |

## 2. `ha_config_list_areas`
List all Home Assistant areas (rooms).
- Parameters: none

## 3. `ha_config_set_area`
Create or update a Home Assistant area (room).
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `name` | no | `string|null` | `null` | Name for the area (required for create, optional for update, e.g., 'Living Room', 'Kitchen') |
| `area_id` | no | `string|null` | `null` | Area ID to update (omit to create new area, use ha_config_list_areas to find IDs) |
| `floor_id` | no | `string|null` | `null` | Floor ID to assign this area to (use ha_config_list_floors to find IDs, empty string to remove) |
| `icon` | no | `string|null` | `null` | Material Design Icon (e.g., 'mdi:sofa', 'mdi:bed', empty string to remove) |
| `aliases` | no | `string|array|null` | `null` | Alternative names for voice assistant recognition (e.g., ['lounge', 'family room'], empty list to clear) |
| `picture` | no | `string|null` | `null` | URL to a picture representing the area (empty string to remove) |

## 4. `ha_config_remove_area`
Delete a Home Assistant area.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `area_id` | yes | `string` | `` | Area ID to delete (use ha_config_list_areas to find IDs) |

## 5. `ha_config_list_floors`
List all Home Assistant floors.
- Parameters: none

## 6. `ha_config_set_floor`
Create or update a Home Assistant floor.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `name` | no | `string|null` | `null` | Name for the floor (required for create, optional for update, e.g., 'Ground Floor', 'Basement') |
| `floor_id` | no | `string|null` | `null` | Floor ID to update (omit to create new floor, use ha_config_list_floors to find IDs) |
| `level` | no | `integer|null` | `null` | Numeric level for ordering (0=ground, 1=first, -1=basement, etc.) |
| `icon` | no | `string|null` | `null` | Material Design Icon (e.g., 'mdi:home-floor-1', 'mdi:home-floor-b', empty string to remove) |
| `aliases` | no | `string|array|null` | `null` | Alternative names for voice assistant recognition (e.g., ['downstairs', 'main level'], empty list to clear) |

## 7. `ha_config_remove_floor`
Delete a Home Assistant floor.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `floor_id` | yes | `string` | `` | Floor ID to delete (use ha_config_list_floors to find IDs) |

## 8. `ha_get_blueprint`
Get blueprint information - list all blueprints or get details for a specific one.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `path` | no | `string|null` | `null` | Blueprint path to get details for (e.g., 'homeassistant/motion_light.yaml'). If omitted, lists all blueprints in the ... |
| `domain` | no | `string` | `automation` | Blueprint domain: 'automation' or 'script' |

## 9. `ha_import_blueprint`
Import a blueprint from a URL.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `url` | yes | `string` | `` | URL to import blueprint from (GitHub, Home Assistant Community, or direct YAML URL) |

## 10. `ha_report_issue`
Collect diagnostic information for filing issue reports or feedback.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `tool_call_count` | no | `integer` | `10` | Number of tool calls made since the issue started. This determines how many log entries to include. Count how many ha... |

## 11. `ha_config_get_calendar_events`
Retrieve calendar events from a calendar entity.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_id` | yes | `string` | `` | Calendar entity ID (e.g., 'calendar.family') |
| `start` | no | `string|null` | `null` | Start datetime in ISO format (default: now) |
| `end` | no | `string|null` | `null` | End datetime in ISO format (default: 7 days from start) |
| `max_results` | no | `integer` | `20` | Maximum number of events to return |

## 12. `ha_config_set_calendar_event`
Create a new event in a calendar.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_id` | yes | `string` | `` | Calendar entity ID (e.g., 'calendar.family') |
| `summary` | yes | `string` | `` | Event title/summary |
| `start` | yes | `string` | `` | Event start datetime in ISO format |
| `end` | yes | `string` | `` | Event end datetime in ISO format |
| `description` | no | `string|null` | `null` | Optional event description |
| `location` | no | `string|null` | `null` | Optional event location |

## 13. `ha_config_remove_calendar_event`
Delete an event from a calendar.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_id` | yes | `string` | `` | Calendar entity ID (e.g., 'calendar.family') |
| `uid` | yes | `string` | `` | Unique identifier of the event to delete |
| `recurrence_id` | no | `string|null` | `null` | Optional recurrence ID for recurring events |
| `recurrence_range` | no | `string|null` | `null` | Optional recurrence range ('THIS_AND_FUTURE' to delete this and future occurrences) |

## 14. `ha_get_camera_image`
Retrieve a snapshot image from a Home Assistant camera entity.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_id` | yes | `string` | `` |  |
| `width` | no | `integer|null` | `null` |  |
| `height` | no | `integer|null` | `null` |  |

## 15. `ha_config_get_automation`
Retrieve Home Assistant automation configuration.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `identifier` | yes | `string` | `` | Automation entity_id (e.g., 'automation.morning_routine') or unique_id |

## 16. `ha_config_set_automation`
Create or update a Home Assistant automation.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `config` | yes | `string|object` | `` | Complete automation configuration with required fields: 'alias', 'trigger', 'action'. Optional: 'description', 'condi... |
| `identifier` | no | `string|null` | `null` | Automation entity_id or unique_id for updates. Omit to create new automation with generated unique_id. |
| `wait` | no | `boolean|string` | `True` | Wait for automation to be queryable before returning. Default: True. Set to False for bulk operations. |

## 17. `ha_config_remove_automation`
Delete a Home Assistant automation.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `identifier` | yes | `string` | `` | Automation entity_id (e.g., 'automation.old_automation') or unique_id to delete |
| `wait` | no | `boolean|string` | `True` | Wait for automation to be fully removed before returning. Default: True. |

## 18. `ha_config_get_dashboard`
Get dashboard info - list all dashboards or get config for a specific one.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `url_path` | no | `string|null` | `null` | Dashboard URL path (e.g., 'lovelace-home'). Use 'default' for default dashboard. If omitted with list_only=True, list... |
| `list_only` | no | `boolean` | `False` | If True, list all dashboards instead of getting config. When True, url_path is ignored. |
| `force_reload` | no | `boolean` | `False` | Force reload from storage (bypass cache) |

## 19. `ha_config_set_dashboard`
Create or update a Home Assistant dashboard.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `url_path` | yes | `string` | `` | Dashboard URL path (e.g., 'my-dashboard'). Use 'default' or 'lovelace' for the default dashboard. New dashboards must... |
| `config` | no | `string|object|null` | `null` | Dashboard configuration with views and cards. Can be dict or JSON string. Omit or set to None to create dashboard wit... |
| `jq_transform` | no | `string|null` | `null` | jq expression to transform existing dashboard config. Mutually exclusive with config and python_transform. Requires c... |
| `python_transform` | no | `string|null` | `null` | Python expression to transform existing dashboard config. Mutually exclusive with config and jq_transform. Requires c... |
| `config_hash` | no | `string|null` | `null` | Config hash from ha_config_get_dashboard for optimistic locking. REQUIRED for jq_transform (validates dashboard uncha... |
| `title` | no | `string|null` | `null` | Dashboard display name shown in sidebar |
| `icon` | no | `string|null` | `null` | MDI icon name (e.g., 'mdi:home', 'mdi:cellphone'). Defaults to 'mdi:view-dashboard' |
| `require_admin` | no | `boolean` | `False` | Restrict dashboard to admin users only |
| `show_in_sidebar` | no | `boolean` | `True` | Show dashboard in sidebar navigation |

## 20. `ha_config_update_dashboard_metadata`
Update dashboard metadata (title, icon, permissions) without changing content.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `dashboard_id` | yes | `string` | `` | Dashboard ID (typically same as url_path) |
| `title` | no | `string|null` | `null` | New dashboard title |
| `icon` | no | `string|null` | `null` | New MDI icon name |
| `require_admin` | no | `boolean|null` | `null` | Update admin requirement |
| `show_in_sidebar` | no | `boolean|null` | `null` | Update sidebar visibility |

## 21. `ha_config_delete_dashboard`
Delete a storage-mode dashboard completely.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `dashboard_id` | yes | `string` | `` | Dashboard ID to delete (typically same as url_path) |

## 22. `ha_get_dashboard_guide`
Get comprehensive guide for designing Home Assistant dashboards.
- Parameters: none

## 23. `ha_get_card_types`
Get list of all available Home Assistant dashboard card types.
- Parameters: none

## 24. `ha_get_card_documentation`
Fetch detailed documentation for a specific dashboard card type.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `card_type` | yes | `string` | `` | Card type name (e.g., 'light', 'thermostat', 'entity'). Use ha_get_card_types() to see all available types. |

## 25. `ha_dashboard_find_card`
Find cards in a dashboard by entity_id, type, or heading text.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `url_path` | no | `string|null` | `null` | Dashboard URL path, e.g. 'lovelace-home'. Omit for default. |
| `entity_id` | no | `string|null` | `null` | Find cards by entity ID. Supports wildcards, e.g. 'sensor.temperature_*'. Matches cards with this entity in 'entity' ... |
| `card_type` | no | `string|null` | `null` | Find cards by type, e.g. 'tile', 'button', 'heading'. |
| `heading` | no | `string|null` | `null` | Find cards by heading/title text (case-insensitive partial match). Useful for finding section headings (type: 'headin... |
| `include_config` | no | `boolean` | `False` | Include full card configuration in results (increases output size). |

## 26. `ha_create_config_entry_helper`
Create Config Entry Flow helper (template, group, utility_meter, etc.).
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `helper_type` | yes | `string` | `` | Helper type |
| `config` | yes | `string|object` | `` | Helper config (JSON or dict) |

## 27. `ha_get_helper_schema`
Get configuration schema for a helper type.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `helper_type` | yes | `string` | `` | Helper type |

## 28. `ha_config_list_helpers`
List all Home Assistant helpers of a specific type with their configurations.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `helper_type` | yes | `string` | `` | Type of helper entity to list |

## 29. `ha_config_set_helper`
Create or update Home Assistant helper entities.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `helper_type` | yes | `string` | `` | Type of helper entity to create or update |
| `name` | yes | `string` | `` | Display name for the helper |
| `helper_id` | no | `string|null` | `null` | Helper ID for updates (e.g., 'my_button' or 'input_button.my_button'). If not provided, creates a new helper. |
| `icon` | no | `string|null` | `null` | Material Design Icon (e.g., 'mdi:bell', 'mdi:toggle-switch') |
| `area_id` | no | `string|null` | `null` | Area/room ID to assign the helper to |
| `labels` | no | `string|array|null` | `null` | Labels to categorize the helper |
| `min_value` | no | `number|null` | `null` | Minimum value (input_number/counter) or minimum length (input_text) |
| `max_value` | no | `number|null` | `null` | Maximum value (input_number/counter) or maximum length (input_text) |
| `step` | no | `number|null` | `null` | Step/increment value for input_number or counter |
| `unit_of_measurement` | no | `string|null` | `null` | Unit of measurement for input_number (e.g., '°C', '%', 'W') |
| `options` | no | `string|array|null` | `null` | List of options for input_select (required for input_select) |
| `initial` | no | `string|integer|null` | `null` | Initial value for the helper (input_select, input_text, input_boolean, input_datetime, counter) |
| `mode` | no | `string|null` | `null` | Display mode: 'box'/'slider' for input_number, 'text'/'password' for input_text |
| `has_date` | no | `boolean|null` | `null` | Include date component for input_datetime |
| `has_time` | no | `boolean|null` | `null` | Include time component for input_datetime |
| `restore` | no | `boolean|null` | `null` | Restore state after restart (counter, timer). Defaults to True for counter, False for timer |
| `duration` | no | `string|null` | `null` | Default duration for timer in format 'HH:MM:SS' or seconds (e.g., '0:05:00' for 5 minutes) |
| `monday` | no | `array|null` | `null` | Schedule time ranges for Monday. List of {'from': 'HH:MM', 'to': 'HH:MM'} dicts. Optional 'data' dict for additional ... |
| `tuesday` | no | `array|null` | `null` | Schedule time ranges for Tuesday. List of {'from': 'HH:MM', 'to': 'HH:MM'} dicts. Optional 'data' dict for additional... |
| `wednesday` | no | `array|null` | `null` | Schedule time ranges for Wednesday. List of {'from': 'HH:MM', 'to': 'HH:MM'} dicts. Optional 'data' dict for addition... |
| `thursday` | no | `array|null` | `null` | Schedule time ranges for Thursday. List of {'from': 'HH:MM', 'to': 'HH:MM'} dicts. Optional 'data' dict for additiona... |
| `friday` | no | `array|null` | `null` | Schedule time ranges for Friday. List of {'from': 'HH:MM', 'to': 'HH:MM'} dicts. Optional 'data' dict for additional ... |
| `saturday` | no | `array|null` | `null` | Schedule time ranges for Saturday. List of {'from': 'HH:MM', 'to': 'HH:MM'} dicts. Optional 'data' dict for additiona... |
| `sunday` | no | `array|null` | `null` | Schedule time ranges for Sunday. List of {'from': 'HH:MM', 'to': 'HH:MM'} dicts. Optional 'data' dict for additional ... |
| `latitude` | no | `number|null` | `null` | Latitude for zone (required for zone) |
| `longitude` | no | `number|null` | `null` | Longitude for zone (required for zone) |
| `radius` | no | `number|null` | `null` | Radius in meters for zone (default: 100) |
| `passive` | no | `boolean|null` | `null` | Passive zone (won't trigger state changes for person entities) |
| `user_id` | no | `string|null` | `null` | User ID to link to person entity |
| `device_trackers` | no | `array|null` | `null` | List of device_tracker entity IDs for person |
| `picture` | no | `string|null` | `null` | Picture URL for person entity |
| `tag_id` | no | `string|null` | `null` | Tag ID for tag (auto-generated if not provided) |
| `description` | no | `string|null` | `null` | Description for tag |
| `wait` | no | `boolean|string` | `True` | Wait for helper entity to be queryable before returning. Default: True. Set to False for bulk operations. |

## 30. `ha_config_remove_helper`
Delete a Home Assistant helper entity.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `helper_type` | yes | `string` | `` | Type of helper entity to delete |
| `helper_id` | yes | `string` | `` | Helper ID to delete (e.g., 'my_button' or 'input_button.my_button') |
| `wait` | no | `boolean|string` | `True` | Wait for helper entity to be fully removed before returning. Default: True. |

## 31. `ha_config_info`
Get information about Home Assistant configuration access via ha-mcp.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `config_type` | no | `string` | `general` | Type of configuration information to retrieve. Options: 'general' (default), 'automation', 'script', 'dashboard', 'in... |

## 32. `ha_config_get_script`
Retrieve Home Assistant script configuration.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `script_id` | yes | `string` | `` | Script identifier (e.g., 'morning_routine') |

## 33. `ha_config_set_script`
Create or update a Home Assistant script.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `script_id` | yes | `string` | `` | Script identifier (e.g., 'morning_routine') |
| `config` | yes | `string|object` | `` | Script configuration dictionary. Must include EITHER 'sequence' (for regular scripts) OR 'use_blueprint' (for bluepri... |
| `wait` | no | `boolean|string` | `True` | Wait for script to be queryable before returning. Default: True. Set to False for bulk operations. |

## 34. `ha_config_remove_script`
Delete a Home Assistant script.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `script_id` | yes | `string` | `` | Script identifier to delete (e.g., 'old_script') |
| `wait` | no | `boolean|string` | `True` | Wait for script to be fully removed before returning. Default: True. |

## 35. `ha_set_entity`
Update entity properties in the entity registry.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_id` | yes | `string|array` | `` | Entity ID or list of entity IDs to update. Bulk operations (list) only support labels and expose_to parameters. |
| `area_id` | no | `string|null` | `null` | Area/room ID to assign the entity to. Use empty string '' to unassign from current area. Single entity only. |
| `name` | no | `string|null` | `null` | Display name for the entity. Use empty string '' to remove custom name and revert to default. Single entity only. |
| `icon` | no | `string|null` | `null` | Icon for the entity (e.g., 'mdi:thermometer'). Use empty string '' to remove custom icon. Single entity only. |
| `enabled` | no | `boolean|string|null` | `null` | True to enable the entity, False to disable it. Single entity only. |
| `hidden` | no | `boolean|string|null` | `null` | True to hide the entity from UI, False to show it. Single entity only. |
| `aliases` | no | `string|array|null` | `null` | List of voice assistant aliases for the entity (replaces existing aliases). Single entity only. |
| `labels` | no | `string|array|null` | `null` | List of label IDs for the entity. Behavior depends on label_operation parameter. Supports bulk operations. |
| `label_operation` | no | `string` | `set` | How to apply labels: 'set' replaces all labels, 'add' adds to existing, 'remove' removes specified labels. |
| `expose_to` | no | `string|object|null` | `null` | Control voice assistant exposure. Pass a dict mapping assistant IDs to booleans. Valid assistants: 'conversation' (As... |

## 36. `ha_get_entity`
Get entity registry information for one or more entities.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_id` | yes | `string|array` | `` | Entity ID or list of entity IDs to retrieve (e.g., 'sensor.temperature' or ['light.living_room', 'switch.porch']) |

## 37. `ha_config_list_groups`
List all Home Assistant entity groups with their member entities.
- Parameters: none

## 38. `ha_config_set_group`
Create or update a Home Assistant entity group.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `object_id` | yes | `string` | `` | Group identifier without 'group.' prefix (e.g., 'living_room_lights') |
| `entities` | no | `array|null` | `null` | List of entity IDs for the group. Required when creating new group. When updating, replaces all entities (mutually ex... |
| `name` | no | `string|null` | `null` | Friendly display name for the group |
| `icon` | no | `string|null` | `null` | Material Design Icon (e.g., 'mdi:lightbulb-group') |
| `all_on` | no | `boolean|null` | `null` | If True, all entities must be on for group to be on (default: False) |
| `add_entities` | no | `array|null` | `null` | Add these entities to an existing group (mutually exclusive with entities) |
| `remove_entities` | no | `array|null` | `null` | Remove these entities from an existing group (mutually exclusive with entities) |

## 39. `ha_config_remove_group`
Remove a Home Assistant entity group.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `object_id` | yes | `string` | `` | Group identifier without 'group.' prefix (e.g., 'living_room_lights') |

## 40. `ha_hacs_info`
Get HACS status, version, and enabled categories.
- Parameters: none

## 41. `ha_hacs_list_installed`
List installed HACS repositories with focused, small response.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `category` | no | `string|null` | `null` | Filter by category: 'integration', 'lovelace', 'theme', 'appdaemon', or 'python_script'. Use None for all categories. |

## 42. `ha_hacs_search`
Search HACS store for repositories by keyword with pagination.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `query` | yes | `string` | `` |  |
| `category` | no | `string|null` | `null` | Filter by category (optional) |
| `max_results` | no | `integer|string` | `10` | Maximum number of results to return (default: 10, max: 100) |
| `offset` | no | `integer|string` | `0` | Number of results to skip for pagination (default: 0) |

## 43. `ha_hacs_repository_info`
Get detailed repository information including README and documentation.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `repository_id` | yes | `string` | `` |  |

## 44. `ha_hacs_add_repository`
Add a custom GitHub repository to HACS.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `repository` | yes | `string` | `` |  |
| `category` | yes | `string` | `` | Repository category (required) |

## 45. `ha_hacs_download`
Download and install a HACS repository.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `repository_id` | yes | `string` | `` |  |
| `version` | no | `string|null` | `null` | Specific version to install (e.g., 'v1.2.3'). If not specified, installs the latest version. |

## 46. `ha_get_history`
Retrieve raw state change history for entities (last ~10 days).
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_ids` | yes | `string|array` | `` | Entity ID(s) to query. Can be a single ID, comma-separated string, or JSON array. |
| `start_time` | no | `string|null` | `null` | Start time: ISO datetime or relative (e.g., '24h', '7d', '2w'). Default: 24h ago |
| `end_time` | no | `string|null` | `null` | End time: ISO datetime. Default: now |
| `minimal_response` | no | `boolean` | `True` | Return only states/timestamps without attributes. Default: true |
| `significant_changes_only` | no | `boolean` | `True` | Filter to significant state changes only. Default: true |
| `limit` | no | `integer|string|null` | `null` | Max state changes per entity. Default: 100, Max: 1000 |

## 47. `ha_get_statistics`
Retrieve pre-aggregated long-term statistics for trend analysis.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_ids` | yes | `string|array` | `` | Entity ID(s) to query. Must have state_class attribute. Can be single ID, comma-separated, or JSON array. |
| `start_time` | no | `string|null` | `null` | Start time: ISO datetime or relative (e.g., '30d', '6m', '12m'). Default: 30d ago |
| `end_time` | no | `string|null` | `null` | End time: ISO datetime. Default: now |
| `period` | no | `string` | `day` | Aggregation period: '5minute', 'hour', 'day', 'week', 'month'. Default: 'day' |
| `statistic_types` | no | `string|array|null` | `null` | Statistics types: 'mean', 'min', 'max', 'sum', 'state', 'change'. Default: all |

## 48. `ha_get_integration`
Get integration (config entry) information - list all or get a specific one.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entry_id` | no | `string|null` | `null` | Config entry ID to get details for. If omitted, lists all integrations. |
| `query` | no | `string|null` | `null` | When listing, fuzzy search by domain or title. |
| `domain` | no | `string|null` | `null` | Filter by integration domain (e.g. 'template', 'group'). When set, includes the full options/configuration for each e... |
| `include_options` | no | `boolean|string` | `False` | Include the options object for each entry. Automatically enabled when domain filter is set. Useful for auditing templ... |

## 49. `ha_set_integration_enabled`
Enable/disable integration (config entry).
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entry_id` | yes | `string` | `` | Config entry ID |
| `enabled` | yes | `boolean|string` | `` | True to enable, False to disable |

## 50. `ha_delete_config_entry`
Delete config entry permanently. Requires confirm=True.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entry_id` | yes | `string` | `` | Config entry ID |
| `confirm` | no | `boolean|string` | `False` | Must be True to confirm deletion |

## 51. `ha_config_get_label`
Get label info - list all labels or get a specific one by ID.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `label_id` | no | `string|null` | `null` | ID of the label to retrieve. If omitted, lists all labels. |

## 52. `ha_config_set_label`
Create or update a Home Assistant label.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `name` | yes | `string` | `` | Display name for the label |
| `label_id` | no | `string|null` | `null` | Label ID for updates. If not provided, creates a new label. |
| `color` | no | `string|null` | `null` | Color for the label (e.g., 'red', 'blue', 'green', or hex like '#FF5733') |
| `icon` | no | `string|null` | `null` | Material Design Icon (e.g., 'mdi:tag', 'mdi:label') |
| `description` | no | `string|null` | `null` | Description of the label's purpose |

## 53. `ha_config_remove_label`
Delete a Home Assistant label.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `label_id` | yes | `string` | `` | ID of the label to delete |

## 54. `ha_rename_entity`
Rename a Home Assistant entity by changing its entity_id.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_id` | yes | `string` | `` | Current entity ID to rename (e.g., 'light.old_name') |
| `new_entity_id` | yes | `string` | `` | New entity ID (e.g., 'light.new_name'). Domain must match the original. |
| `name` | no | `string|null` | `null` | Optional: New friendly name for the entity |
| `icon` | no | `string|null` | `null` | Optional: New icon (e.g., 'mdi:lightbulb') |
| `preserve_voice_exposure` | no | `boolean|string|null` | `null` | Migrate voice assistant exposure settings to the new entity_id. Defaults to True. Set to False to skip exposure migra... |

## 55. `ha_get_device`
Get device information - list all devices or get details for a specific one.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `device_id` | no | `string|null` | `null` | Device ID to retrieve details for. If omitted, lists devices. |
| `entity_id` | no | `string|null` | `null` | Entity ID to find the associated device for (e.g., 'light.living_room') |
| `integration` | no | `string|null` | `null` | Filter devices by integration: 'zha', 'zigbee2mqtt', 'mqtt', 'hue', etc. |
| `area_id` | no | `string|null` | `null` | Filter devices by area ID (e.g., 'living_room') |
| `manufacturer` | no | `string|null` | `null` | Filter devices by manufacturer name (e.g., 'Philips') |

## 56. `ha_update_device`
Update device properties such as name, area, disabled state, or labels.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `device_id` | yes | `string` | `` | Device ID to update |
| `name` | no | `string|null` | `null` | New display name for the device (sets name_by_user) |
| `area_id` | no | `string|null` | `null` | Area/room ID to assign the device to. Use empty string '' to unassign. |
| `disabled_by` | no | `string|null` | `null` | Set to 'user' to disable, or None/empty string to enable |
| `labels` | no | `string|array|null` | `null` | Labels to assign to the device (replaces existing labels) |

## 57. `ha_remove_device`
Remove an orphaned device from the Home Assistant device registry.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `device_id` | yes | `string` | `` | Device ID to remove from the registry |

## 58. `ha_rename_entity_and_device`
Convenience tool to rename both an entity and its associated device in one operation.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_id` | yes | `string` | `` | Entity ID to rename (e.g., 'light.bedroom_lamp'). Used to find associated device. |
| `new_entity_id` | yes | `string` | `` | New entity ID (e.g., 'light.master_bedroom_lamp'). Domain must match. |
| `new_device_name` | no | `string|null` | `null` | New display name for the device. If not provided, device name is not changed. |
| `new_entity_name` | no | `string|null` | `null` | New friendly name for the entity. If not provided, entity name is not changed. |
| `preserve_voice_exposure` | no | `boolean|string|null` | `null` | Migrate voice assistant exposure settings to the new entity_id. Defaults to True. |

## 59. `ha_config_list_dashboard_resources`
List all Lovelace dashboard resources (custom cards, themes, CSS/JS).
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `include_content` | no | `boolean` | `False` | Include full decoded content for inline resources. Default False to save tokens (shows 150-char preview instead). |

## 60. `ha_config_set_inline_dashboard_resource`
Create or update an inline dashboard resource from code.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `content` | yes | `string` | `` | JavaScript or CSS code to host (max ~24KB) |
| `resource_type` | no | `string` | `module` | Resource type: 'module' for ES6 JavaScript (custom cards), 'css' for stylesheets |
| `resource_id` | no | `string|null` | `null` | Resource ID to update. If omitted, creates a new resource. Get IDs from ha_config_list_dashboard_resources() |

## 61. `ha_config_set_dashboard_resource`
Create or update a dashboard resource from a URL.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `url` | yes | `string` | `` | URL of the resource. Can be: /local/file.js (www/ directory), /hacsfiles/component/file.js (HACS), https://cdn.exampl... |
| `resource_type` | no | `string` | `module` | Resource type: 'module' for ES6 modules (modern cards), 'js' for legacy JavaScript, 'css' for stylesheets |
| `resource_id` | no | `string|null` | `null` | Resource ID to update. If omitted, creates a new resource. Get IDs from ha_config_list_dashboard_resources() |

## 62. `ha_config_delete_dashboard_resource`
Delete a dashboard resource.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `resource_id` | yes | `string` | `` | Resource ID to delete. Get from ha_config_list_dashboard_resources() |

## 63. `ha_search_entities`
Comprehensive entity search with fuzzy matching, domain/area filtering, and optional grouping.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `query` | yes | `string` | `` |  |
| `domain_filter` | no | `string|null` | `null` |  |
| `area_filter` | no | `string|null` | `null` |  |
| `limit` | no | `integer` | `10` |  |
| `offset` | no | `integer|string` | `0` | Number of results to skip for pagination (default: 0) |
| `group_by_domain` | no | `boolean|string` | `False` |  |

## 64. `ha_get_overview`
Get AI-friendly system overview with intelligent categorization.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `detail_level` | no | `string` | `minimal` | 'minimal': 10 entities per domain sample (default); 'standard': ALL entities per domain (friendly_name only); 'full':... |
| `max_entities_per_domain` | no | `integer|null` | `null` | Override max entities per domain (None = all). Minimal defaults to 10. |
| `include_state` | no | `boolean|string|null` | `null` | Include state field for entities (None = auto based on level). Full defaults to True. |
| `include_entity_id` | no | `boolean|string|null` | `null` | Include entity_id field for entities (None = auto based on level). Full defaults to True. |

## 65. `ha_deep_search`
Deep search across automation, script, and helper definitions.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `query` | yes | `string` | `` |  |
| `search_types` | no | `string|array|null` | `null` | Types to search: 'automation', 'script', 'helper'. Pass as list or JSON array string. Default: all types. |
| `limit` | no | `integer` | `5` |  |
| `offset` | no | `integer` | `0` |  |
| `include_config` | no | `boolean|string` | `False` | Include full config in results. Default: False (returns summary only). Use ha_config_get_automation/ha_config_get_scr... |

## 66. `ha_get_state`
Get detailed state information for a Home Assistant entity with timezone metadata.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_id` | yes | `string` | `` |  |

## 67. `ha_get_states`
Get state information for multiple Home Assistant entities in a single call.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_ids` | yes | `array` | `` | List of entity IDs to retrieve states for (e.g., ['light.kitchen', 'sensor.temperature']) |

## 68. `ha_call_service`
Execute Home Assistant services to control entities and trigger automations.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `domain` | yes | `string` | `` |  |
| `service` | yes | `string` | `` |  |
| `entity_id` | no | `string|null` | `null` |  |
| `data` | no | `string|object|null` | `null` |  |
| `return_response` | no | `boolean|string` | `False` |  |
| `wait` | no | `boolean|string` | `True` |  |

## 69. `ha_get_operation_status`
Check status of device operation with real-time WebSocket verification.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `operation_id` | yes | `string` | `` |  |
| `timeout_seconds` | no | `integer` | `10` |  |

## 70. `ha_bulk_control`
Control multiple devices with bulk operation support and WebSocket tracking.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `operations` | yes | `string|array` | `` |  |
| `parallel` | no | `boolean|string` | `True` |  |

## 71. `ha_get_bulk_status`
Check status of multiple device control operations.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `operation_ids` | yes | `array` | `` |  |

## 72. `ha_list_services`
List available Home Assistant services with their parameters.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `domain` | no | `string|null` | `null` |  |
| `query` | no | `string|null` | `null` |  |

## 73. `ha_check_config`
Check Home Assistant configuration for errors.
- Parameters: none

## 74. `ha_restart`
Restart Home Assistant.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `confirm` | no | `boolean|string` | `False` |  |

## 75. `ha_reload_core`
Reload Home Assistant configuration without full restart.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `target` | no | `string` | `all` |  |

## 76. `ha_get_system_health`
Get Home Assistant system health information.
- Parameters: none

## 77. `ha_get_todo`
Get todo lists or items - list all todo lists or get items from a specific list.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_id` | no | `string|null` | `null` | Todo list entity ID (e.g., 'todo.shopping_list'). If omitted, lists all todo list entities. |
| `status` | no | `string|null` | `null` | Filter items by status: 'needs_action' for incomplete, 'completed' for done. Only applies when entity_id is provided. |

## 78. `ha_add_todo_item`
Add an item to a Home Assistant todo list.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_id` | yes | `string` | `` | Todo list entity ID (e.g., 'todo.shopping_list') |
| `summary` | yes | `string` | `` | Item text/name to add (e.g., 'Buy milk') |
| `description` | no | `string|null` | `null` | Optional detailed description for the item |
| `due_date` | no | `string|null` | `null` | Optional due date in YYYY-MM-DD format (e.g., '2024-12-25') |
| `due_datetime` | no | `string|null` | `null` | Optional due datetime in ISO format (e.g., '2024-12-25T14:00:00') |

## 79. `ha_update_todo_item`
Update or complete a todo item in Home Assistant.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_id` | yes | `string` | `` | Todo list entity ID (e.g., 'todo.shopping_list') |
| `item` | yes | `string` | `` | Item to update - can be the item UID or the exact item summary/name |
| `rename` | no | `string|null` | `null` | New name/summary for the item |
| `status` | no | `string|null` | `null` | New status: 'completed' to mark done, 'needs_action' to mark incomplete |
| `description` | no | `string|null` | `null` | New description for the item |
| `due_date` | no | `string|null` | `null` | New due date in YYYY-MM-DD format |
| `due_datetime` | no | `string|null` | `null` | New due datetime in ISO format |

## 80. `ha_remove_todo_item`
Remove an item from a Home Assistant todo list.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_id` | yes | `string` | `` | Todo list entity ID (e.g., 'todo.shopping_list') |
| `item` | yes | `string` | `` | Item to remove - can be the item UID or the exact item summary/name |

## 81. `ha_get_automation_traces`
Retrieve execution traces for automations and scripts to debug issues.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `automation_id` | yes | `string` | `` | Automation or script entity_id (e.g., 'automation.motion_light' or 'script.morning_routine') |
| `run_id` | no | `string|null` | `null` | Specific trace run_id to retrieve detailed trace. Omit to list recent traces. |
| `limit` | no | `integer` | `10` | Maximum number of traces to return when listing (default: 10, max: 50) |

## 82. `ha_get_updates`
Get update information - list all updates or get details for a specific one.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_id` | no | `string|null` | `null` | Update entity ID to get details for (e.g., 'update.home_assistant_core_update'). If omitted, lists all available upda... |
| `include_skipped` | no | `boolean|string` | `False` | When listing all updates, include updates that have been skipped (default: False) |

## 83. `ha_get_logbook`
Get Home Assistant logbook entries for the specified time period.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `hours_back` | no | `integer|string` | `1` |  |
| `entity_id` | no | `string|null` | `null` |  |
| `end_time` | no | `string|null` | `null` |  |
| `limit` | no | `integer|string|null` | `null` |  |
| `offset` | no | `integer|string` | `0` |  |

## 84. `ha_eval_template`
Evaluate Jinja2 templates using Home Assistant's template engine.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `template` | yes | `string` | `` |  |
| `timeout` | no | `integer` | `3` |  |
| `report_errors` | no | `boolean|string` | `True` |  |

## 85. `ha_get_domain_docs`
Get comprehensive documentation for Home Assistant entity domains.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `domain` | yes | `string` | `` |  |

## 86. `ha_get_entity_exposure`
Get entity exposure settings - list all or get settings for a specific entity.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `entity_id` | no | `string|null` | `null` | Entity ID to check exposure settings for. If omitted, lists all entities with exposure settings. |
| `assistant` | no | `string|null` | `null` | Filter by assistant: 'conversation', 'cloud.alexa', or 'cloud.google_assistant'. If not specified, returns all. |

## 87. `ha_get_zone`
Get zone information - list all zones or get details for a specific one.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `zone_id` | no | `string|null` | `null` | Zone ID to get details for (from ha_get_zone() list). If omitted, lists all zones. |

## 88. `ha_create_zone`
Create a new Home Assistant zone for presence detection.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `name` | yes | `string` | `` | Display name for the zone |
| `latitude` | yes | `number` | `` | Latitude coordinate of the zone center |
| `longitude` | yes | `number` | `` | Longitude coordinate of the zone center |
| `radius` | no | `number` | `100` | Radius of the zone in meters (default: 100) |
| `icon` | no | `string|null` | `null` | Material Design Icon (e.g., 'mdi:briefcase', 'mdi:school') |
| `passive` | no | `boolean` | `False` | If True, zone will not trigger automations on enter/exit (default: False) |

## 89. `ha_update_zone`
Update an existing Home Assistant zone.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `zone_id` | yes | `string` | `` | Zone ID to update (from ha_get_zone) |
| `name` | no | `string|null` | `null` | New display name for the zone |
| `latitude` | no | `number|null` | `null` | New latitude coordinate |
| `longitude` | no | `number|null` | `null` | New longitude coordinate |
| `radius` | no | `number|null` | `null` | New radius in meters |
| `icon` | no | `string|null` | `null` | New Material Design Icon |
| `passive` | no | `boolean|null` | `null` | New passive mode setting |

## 90. `ha_delete_zone`
Delete a Home Assistant zone.
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `zone_id` | yes | `string` | `` | Zone ID to delete (from ha_get_zone) |

## 91. `ha_backup_create`
Create a fast Home Assistant backup (local only).
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `name` | no | `string|null` | `null` | Backup name (auto-generated if not provided, e.g., 'MCP_Backup_2025-10-05_04:30') |

## 92. `ha_backup_restore`
Restore Home Assistant from a backup (LAST RESORT - use with extreme caution).
| Parameter | Required | Type | Default | Description |
|---|---|---|---|---|
| `backup_id` | yes | `string` | `` | Backup ID to restore (e.g., 'dd7550ed' from backup list or ha_backup_create result) |
| `restore_database` | no | `boolean` | `False` | Restore database (default: false for config-only restore) |


