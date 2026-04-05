# Documentation Index / 文档索引

**Project**: Crisis Investment Researcher  
**Version**: 0.3.0  
**Updated**: 2026-04-05

---

## Quick Navigation / 快速导航

### Getting Started / 开始使用
- **[README.md](README.md)** - Project overview and quick start / 项目概览与快速开始
- **[docs/01-QUICKSTART.md](docs/01-QUICKSTART.md)** - 5-minute setup / 5分钟快速上手

### Learning / 深入学习
- **[docs/02-USAGE.md](docs/02-USAGE.md)** - Complete feature guide / 完整功能指南
- **[docs/03-INTEGRATION.md](docs/03-INTEGRATION.md)** - Claude integration / Claude 集成

### Setup & Development / 部署与开发
- **[docs/04-DEPLOYMENT.md](docs/04-DEPLOYMENT.md)** - Installation and configuration / 安装与配置
- **[docs/05-API-REFERENCE.md](docs/05-API-REFERENCE.md)** - API reference for all modules / 所有模块的 API 参考
- **[docs/07-PROJECT-STRUCTURE.md](docs/07-PROJECT-STRUCTURE.md)** - Architecture and code layout / 项目架构与代码布局

### Troubleshooting / 故障排查
- **[docs/06-TROUBLESHOOTING.md](docs/06-TROUBLESHOOTING.md)** - Common problems and solutions / 常见问题与解决方案

### System Files / 系统文件
- **[SKILL.md](SKILL.md)** - Claude skill discovery file (do not delete) / Claude 技能发现文件（勿删）
- **[.instructions.md](.instructions.md)** - Claude usage instructions / Claude 使用说明
- **[config.yaml](config.yaml)** - Main configuration file / 主配置���件

---

## Reading Paths / 阅读路径

### Beginners / 初学者
1. [README.md](README.md) -- 5 min
2. [01-QUICKSTART.md](docs/01-QUICKSTART.md) -- 5 min
3. [02-USAGE.md](docs/02-USAGE.md) -- 15 min
4. [03-INTEGRATION.md](docs/03-INTEGRATION.md) -- 10 min

### Developers / 开发者
1. [README.md](README.md) -- 5 min
2. [04-DEPLOYMENT.md](docs/04-DEPLOYMENT.md) -- 10 min
3. [05-API-REFERENCE.md](docs/05-API-REFERENCE.md) -- 20 min
4. [07-PROJECT-STRUCTURE.md](docs/07-PROJECT-STRUCTURE.md) -- 10 min

### Troubleshooting / 遇到问题
- [06-TROUBLESHOOTING.md](docs/06-TROUBLESHOOTING.md) -- as needed

---

## File Summary / 文件一览

| File | Purpose / 用途 |
|------|---|
| README.md | Project overview, quick start, feature list / 项目概览 |
| docs/01-QUICKSTART.md | 3 ways to use: Claude Chat, CLI, Python / 三种使用方式 |
| docs/02-USAGE.md | All features: search, research, valuation, validation, export / 全部功能详解 |
| docs/03-INTEGRATION.md | Claude integration architecture and MCP tools / Claude 集成架构 |
| docs/04-DEPLOYMENT.md | Installation, config.yaml setup, dependency guide / 安装与配置指南 |
| docs/05-API-REFERENCE.md | All classes and methods reference / 全部类与方法参考 |
| docs/06-TROUBLESHOOTING.md | Error solutions and debugging guide / 错误排查与调试 |
| docs/07-PROJECT-STRUCTURE.md | Directory layout, data flow, module relationships / 目录结构与数据流 |
| SKILL.md | Claude skill metadata and anti-hallucination rules / Claude 技能元数据 |
| .instructions.md | Claude behavior instructions / Claude 行为指令 |
| config.yaml | All configurable settings with bilingual comments / 所有可配置项 |

---

## Quick Commands / 快速命令

```bash
# Verify setup / 验证安装
python check_integration.py

# CLI search / 命令行搜索
python src/claude_skill.py "Apple stock news"

# Research mode / 研究模式
python src/claude_skill.py "Generate report for AAPL" --research

# JSON output / JSON 输出
python src/claude_skill.py "Tesla analysis" --json
```
