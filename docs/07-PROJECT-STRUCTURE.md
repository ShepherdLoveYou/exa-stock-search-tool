# 📁 项目结构说明

项目文件组织和各部分说明。

---

## 📊 完整项目树

```
d:\MCP project\EXA search MCP\
│
├── 📁 src/                          # 主源代码目录
│   ├── __init__.py
│   ├── stock_searcher.py            # ⭐ 核心搜索类
│   ├── skill_router.py              # ⭐ 智能路由引擎
│   ├── claude_skill.py              # ⭐ Claude接口
│   ├── mcp_server.py                # MCP服务器（可选）
│   │
│   ├── 📁 examples/                 # 示例代码
│   │   ├── __init__.py
│   │   ├── basic_search.py          # 基础搜索演示
│   │   ├── stock_search.py          # 股票搜索演示
│   │   ├── claude_skill_demo.py     # Claude Skill演示
│   │   ├── openai_function_calling.py
│   │   └── anthropic_tool_use.py
│   │
│   └── 📁 utils/                    # 辅助工具
│       ├── __init__.py
│       └── helpers.py               # 工具函数
│
├── 📁 config/                       # 配置文件目录
│   ├── exa_config.json              # Exa API配置
│   └── mcp_config.json              # MCP配置
│
├── 📁 scripts/                      # 设置脚本
│   ├── setup_env.ps1                # 完整环境设置
│   └── install_dependencies.ps1     # 依赖安装
│
├── 📁 docs/                         # 📖 文档目录（新增）
│   ├── 01-QUICKSTART.md             # 快速开始
│   ├── 02-USAGE.md                  # 完整使用指南
│   ├── 03-INTEGRATION.md            # Claude集成指南
│   ├── 04-DEPLOYMENT.md             # 部署指南
│   ├── 05-API-REFERENCE.md          # API参考
│   ├── 06-TROUBLESHOOTING.md        # 故障排查
│   └── 07-PROJECT-STRUCTURE.md      # 项目结构（本文件）
│
├── 📁 venv/                         # Python虚拟环境
│   ├── Scripts/                     # 可执行文件
│   │   ├── python.exe
│   │   ├── pip.exe
│   │   └── Activate.ps1
│   └── Lib/                         # 已安装包
│
├── 📁 .vscode/                      # VS Code配置
│   ├── settings.json                # VS Code设置
│   └── tasks.json                   # 自定义任务
│
├── 📄 README.md                     # 项目说明（根目录）
├── 📄 SKILL.md                      # ⭐ Claude发现文件（必需）
├── 📄 .instructions.md              # ⭐ Claude说明文件（必需）
│
├── 📄 .env                          # ⭐ API Key配置（本地，不提交）
├── 📄 .env.example                  # .env模板
│
├── 📄 requirements.txt              # Python依赖列表
├── 📄 setup.py                      # 包配置
├── 📄 check_integration.py          # 集成检查脚本
│
├── 📄 .gitignore                    # Git忽略规则
│
└── 📄 USAGE_GUIDE.md                # 使用指南（保留）

```

---

## 🎯 核心文件说明

### ⭐ 必需文件

#### 1. `src/stock_searcher.py`
**用途**: 核心搜索功能

**功能**:
- `StockSearcher` 类 - 主搜索引擎
- `search_stock_news()` - 查询股票新闻
- `search_market_analysis()` - 市场分析
- `search_company_info()` - 公司信息
- `search_with_deep_research()` - 深度研究
- `format_results()` - 格式化输出

**关键类**:
```python
class StockSearcher:
    def __init__(self, api_key: Optional[str] = None)
    def search_stock_news(self, ticker: str, num_results: int = 10, include_highlights: bool = True) -> Dict
    def search_market_analysis(self, topic: str, num_results: int = 10, include_highlights: bool = True) -> Dict
    def search_company_info(self, company_name: str, num_results: int = 10, include_highlights: bool = True) -> Dict
    def search_with_deep_research(self, query: str, num_results: int = 10, include_highlights: bool = True) -> Dict
    @staticmethod
    def format_results(results: Dict, max_items: Optional[int] = None) -> str
```

---

#### 2. `src/skill_router.py`
**用途**: 智能查询路由

**功能**:
- `ExaSkillRouter` 类 - 路由引擎
- `detect_search_type()` - 自动类型检测
- `search()` - 执行搜索
- `search_and_format()` - 返回文本结果
- `search_as_json()` - 返回JSON结果

**关键类**:
```python
class ExaSkillRouter:
    def __init__(self, api_key: Optional[str] = None)
    def detect_search_type(self, query: str) -> Tuple[str, float]
    def search(self, query: str, num_results: int = 10) -> Dict
    def search_and_format(self, query: str, num_results: int = 10) -> str
    def search_as_json(self, query: str, num_results: int = 10) -> Dict
```

---

#### 3. `src/claude_skill.py`
**用途**: Claude接口

**功能**:
- `search_stock()` - Claude调用的搜索函数
- `search_stock_json()` - Claude调用的JSON函数
- `main()` - CLI入口

**导出函数**:
```python
def search_stock(query: str, num_results: int = 10) -> str
def search_stock_json(query: str, num_results: int = 10) -> dict
```

---

#### 4. `SKILL.md`
**用途**: Claude自动发现

**内容**:
```yaml
---
description: Search real-time stock market information using Exa neural search
name: exa-stock-search
tags: [web-search, stocks, market-research, finance]
---
```

**重要**: Claude通过此文件自动发现Skill

---

#### 5. `.instructions.md`
**用途**: Claude使用说明

**内容**: 告诉Claude如何使用Skill
- 功能说明
- 支持的查询类型
- 使用示例
- 最佳实践

---

#### 6. `.env`
**用途**: API密钥存储

**内容**:
```env
EXA_API_KEY=your-api-key-here
OPENAI_API_KEY=your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
```

**重要**: 包含敏感信息，不提交到Git

---

### 📖 配置文件

#### `config/exa_config.json`
```json
{
  "api_base": "https://api.exa.ai",
  "search_type": "auto",
  "num_results": 10,
  "highlights": true,
  "max_highlight_length": 4000,
  "timeout": 30
}
```

#### `config/mcp_config.json`
```json
{
  "server_name": "exa-search-mcp",
  "version": "1.0.0",
  "capabilities": ["search_stock", "search_market_analysis", "search_company_info", "search_deep_research"]
}
```

---

### 🔧 脚本文件

#### `scripts/setup_env.ps1`
**用途**: 一键完整设置

**功能**:
- 创建虚拟环境
- 安装依赖
- 验证安装

#### `scripts/install_dependencies.ps1`
**用途**: 仅安装依赖

---

### 📚 示例代码

#### `src/examples/basic_search.py`
基础搜索示例

#### `src/examples/stock_search.py`
股票搜索示例

#### `src/examples/claude_skill_demo.py`
Claude Skill演示

---

## 📋 文件用途矩阵

| 文件 | 用途 | 必需 | 可修改 | 提交Git |
|------|------|------|--------|--------|
| src/stock_searcher.py | 核心搜索 | ✅ | ⚠️ | ✅ |
| src/skill_router.py | 智能路由 | ✅ | ⚠️ | ✅ |
| src/claude_skill.py | Claude接口 | ✅ | ⚠️ | ✅ |
| SKILL.md | Claude发现 | ✅ | ⚠️ | ✅ |
| .instructions.md | Claude说明 | ✅ | ✅ | ✅ |
| .env | API Key | ✅ | ⚠️ | ❌ |
| .env.example | .env模板 | ✅ | ✅ | ✅ |
| requirements.txt | 依赖 | ✅ | ⚠️ | ✅ |
| config/ | 配置 | ✅ | ⚠️ | ✅ |
| venv/ | 虚拟环境 | ✅ | ❌ | ❌ |
| docs/ | 文档 | ❌ | ✅ | ✅ |

---

## 🔄 数据流

### 搜索数据流

```
用户输入
    ↓
Claude Chat / 命令行
    ↓
claude_skill.py (search_stock)
    ↓
skill_router.py (detect_search_type + search)
    ↓
stock_searcher.py (search_* methods)
    ↓
Exa API
    ↓
搜索结果
    ↓
格式化 (format_results)
    ↓
返回给用户
```

---

## 📦 依赖关系

```
Claude Chat (用户界面)
    ↓
SKILL.md + .instructions.md (发现和使用说明)
    ↓
claude_skill.py (导出的函数)
    ↓
skill_router.py (路由逻辑)
    ↓
stock_searcher.py (搜索实现)
    ↓
exa_py (Exa API客户端)
    ↓
anthropic (如需Claude API直接调用)
    ↓
openai (如需OpenAI直接调用)
```

---

## 🚀 使用路径

### 路径1：Claude Chat
```
Claude Chat → SKILL.md → .instructions.md → claude_skill.py
```

### 路径2：命令行
```
命令行 → claude_skill.py → skill_router.py → stock_searcher.py
```

### 路径3：Python代码
```
Python代码 → skill_router或stock_searcher → Exa API
```

---

## 💾 文件大小参考

| 文件 | 大小 |
|------|------|
| src/stock_searcher.py | ~2KB |
| src/skill_router.py | ~3KB |
| src/claude_skill.py | ~1KB |
| SKILL.md | <1KB |
| .instructions.md | ~2KB |
| docs/ (所有文档) | ~50KB |
| venv/ (虚拟环境) | ~200MB |

---

## 🔑 关键文件详解

### 为什么需要这些文件？

| 文件 | 理由 |
|------|------|
| stock_searcher.py | 实现搜索逻辑和Exa API调用 |
| skill_router.py | 智能路由查询到正确的搜索类型 |
| claude_skill.py | 提供Claude可调用的函数接口 |
| SKILL.md | 让Claude自动发现此Skill |
| .instructions.md | 告诉Claude如何使用此Skill |
| .env | 安全存储API密钥 |
| requirements.txt | 记录和安装依赖 |
| docs/ | 完整的文档和参考 |

---

## 🔄 修改指南

### 安全修改
✅ 修改搜索参数 (src/stock_searcher.py中的默认值)
✅ 添加新的搜索方法 (src/stock_searcher.py)
✅ 改进路由检测 (src/skill_router.py)
✅ 更新文档

### 危险修改
❌ 修改Claude导出函数签名 (src/claude_skill.py的search_stock函数)
❌ 修改SKILL.md的name字段
❌ 删除必要的模块
❌ 修改.env (仅设置API Key)

---

## 📚 相关文档

- [快速开始](01-QUICKSTART.md)
- [完整使用](02-USAGE.md)
- [Claude集成](03-INTEGRATION.md)
- [部署指南](04-DEPLOYMENT.md)
- [API参考](05-API-REFERENCE.md)
- [故障排查](06-TROUBLESHOOTING.md)

---

## ✅ 项目结构验证

运行此命令验证所有必要文件存在：

```powershell
python check_integration.py
```

**预期输出**:
```
✅ SKILL.md exists
✅ .instructions.md exists
✅ Core modules import successfully
✅ API Key configured
✅ All dependencies installed
✅ All checks passed!
```

---

## 🎯 快速导航

**我想...**

- **学习基础** → [01-QUICKSTART.md](01-QUICKSTART.md)
- **详细使用** → [02-USAGE.md](02-USAGE.md)
- **集成Claude** → [03-INTEGRATION.md](03-INTEGRATION.md)
- **设置环境** → [04-DEPLOYMENT.md](04-DEPLOYMENT.md)
- **查看API** → [05-API-REFERENCE.md](05-API-REFERENCE.md)
- **解决问题** → [06-TROUBLESHOOTING.md](06-TROUBLESHOOTING.md)
- **了解结构** → [07-PROJECT-STRUCTURE.md](07-PROJECT-STRUCTURE.md) (本文件)
