# Quick Start Guide / 快速开始指南 (5 min)

**Crisis Investment Researcher v0.3.0**
**Get the system running in 5 minutes.**

---

## Prerequisites / 前置条件

- Python >= 3.9
- Exa API key (get it from https://dashboard.exa.ai/api-keys)

### Install dependencies / 安装依赖

```powershell
pip install -r requirements.txt
```

### Configure API key / 配置 API 密钥

**Option A: config.yaml (recommended / 推荐)**

Open `config.yaml` in the project root and fill in your key:

```yaml
api_keys:
  exa: "your-exa-api-key-here"    # Required / 必填
  openai: ""                       # Optional / 选填
  anthropic: ""                    # Optional / 选填
```

**Option B: .env file**

```
EXA_API_KEY=your-exa-api-key-here
```

**Option C: system environment variable**

```powershell
$env:EXA_API_KEY="your-exa-api-key-here"
```

Priority order: environment variable > config.yaml > .env
(优先级: 环境变量 > config.yaml > .env)

---

## Method 1: Claude Chat (recommended / 推荐)

### 3 steps to start / 三步开始

**Step 1** -- Open the project in VS Code

```
Shortcut: Ctrl + K, Ctrl + O
Select: d:\MCP project\EXA search MCP
Click: Select Folder
```

**Step 2** -- Open Claude Chat

```
Shortcut: Ctrl + L
```

**Step 3** -- Type a query in natural language

```
"Generate research report for Apple (AAPL)"
"Analyze AI stocks market trend"
"Calculate DCF valuation for Tesla with FCF=8B, growth=20%"
"Check data freshness for this report"
```

Claude automatically detects intent and dispatches to the correct tool -- search, research report, valuation, freshness check, or export.

---

## Method 2: Command Line / 命令行

### Basic search / 基础搜索

```powershell
python src/claude_skill.py "Apple stock news"
```

### Research mode / 研究模式

```powershell
python src/claude_skill.py "Generate report for AAPL" --research
```

### JSON output / JSON 输出

```powershell
python src/claude_skill.py "Tesla market analysis" --json
```

### Combined options / 组合选项

```powershell
python src/claude_skill.py "AI stocks analysis" --json --results 5
```

### All CLI flags / 所有命令行参数

| Flag          | Description                      | Example              |
|---------------|----------------------------------|----------------------|
| `--json`      | Output in JSON format / JSON输出  | `--json`             |
| `--research`  | Research routing mode / 研究模式  | `--research`         |
| `--results N` | Limit result count / 限制结果数   | `--results 5`        |

---

## Method 3: Python Code / Python 代码

### Search with UnifiedSkillRouter / 使用统一路由搜索

```python
from src.server.skill_router import UnifiedSkillRouter

router = UnifiedSkillRouter()

# Text formatted results / 文本格式结果
result = router.search_and_format("Apple stock news")
print(result)

# JSON formatted results / JSON 格式结果
json_result = router.search_as_json("Tesla market analysis")
print(json_result)

# Full research routing (report, valuation, freshness, etc.)
# 完整研究路由 (报告/估值/时效性等)
output = router.route("Generate report for AAPL")
print(output)
```

### Direct searcher access / 直接使用搜索器

```python
from src.search.exa_searcher import StockSearcher

searcher = StockSearcher()

news = searcher.search_stock_news("AAPL", num_results=5)
analysis = searcher.search_market_analysis("AI stocks", num_results=5)
company = searcher.search_company_info("Microsoft", num_results=5)
deep = searcher.search_with_deep_research("semiconductor industry", num_results=5)

print(StockSearcher.format_results(news))
```

---

## Verify installation / 验证安装

```powershell
# Check MCP server initializes correctly / 检查 MCP 服务器是否正常初始化
python -m src.server.mcp_server

# Expected output:
# Exa MCP Server initialized successfully!
# Available tools (14): ...
```

---

## Supported query types / 支持的查询类型

| Type / 类型           | Example / 示例                                  | Route target     |
|-----------------------|-------------------------------------------------|------------------|
| Stock news / 股票新闻  | "AAPL latest news", "Tesla stock update"        | search_stock_news |
| Market analysis / 分析 | "AI stocks market analysis", "sector trends"    | search_market_analysis |
| Company info / 公司    | "Microsoft company profile", "Google earnings"  | search_company_info |
| Deep research / 深度   | "Semiconductor industry deep research"          | deep_research |
| Report gen / 生成报告  | "Generate report for AAPL", "Research UNI"      | generate_research_report |
| Valuation / 估值       | "DCF valuation", "Graham formula"               | calculate_valuation |
| Freshness / 时效性     | "Check data freshness"                          | check_report_freshness |
| Position / 仓位        | "Position sizing 200 95"                        | get_position_sizing |
| Checklist / 清单       | "Do-not-invest checklist"                       | get_do_not_invest_checklist |

---

## Troubleshooting / 常见问题

**Q: Encoding error on Windows? / 编码错误？**

```powershell
$env:PYTHONIOENCODING="utf-8"
python src/claude_skill.py "query"
```

**Q: API key not found? / API 密钥找不到？**

Check the priority chain: env var > config.yaml > .env.
Make sure at least one of these is set.
(确认至少一处已正确填写 API 密钥。)

**Q: Module import error? / 模块导入错误？**

```powershell
pip install -r requirements.txt
```

Make sure you run from the project root directory.
(确保在项目根目录下运行。)

---

## Next steps / 下一步

- [Complete usage guide / 完整使用指南](02-USAGE.md)
- [Claude integration guide / Claude 集成指南](03-INTEGRATION.md)
