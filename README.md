# skills-ha-mcp-control

用于通过 `ha-mcp` 查询和控制 Home Assistant 的 Codex Skill。

## 在其他电脑上安装

### 前提

- 目标电脑已安装并可运行 Codex
- 目标电脑可以访问 GitHub

### 安装命令

```bash
python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo Mr-several/skills-ha-mcp-control \
  --path .
```

### 生效

安装完成后，重启 Codex 以加载新 skill。

## 更新到最新版本

安装脚本默认不会覆盖同名目录。更新时建议先删除旧版本再重装：

```bash
rm -rf "$CODEX_HOME/skills/skills-ha-mcp-control"
python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo Mr-several/skills-ha-mcp-control \
  --path .
```
