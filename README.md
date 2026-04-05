# Crisis Investment Researcher / 危机投资研究器

Real-time financial research powered by Exa Search API + Claude integration.
Structured investment reports with 10+ valuation methods, data validation, and dual Markdown/PDF export.

基于 Exa 搜索 API 的实时金融研究工具，与 Claude 深度集成。
支持三种投研框架、10+ 估值方法、数据交叉验证，以及 Markdown/PDF 双格式导出。

---

## Quick Start / 快速开始

### Step 1: Get your API key / 获取 API 密钥

Visit https://dashboard.exa.ai/api-keys, sign up and copy your key.

访问 https://dashboard.exa.ai/api-keys ，注册并复制你的密钥。

### Step 2: Configure / 配置

**Option A: Edit `config.yaml` (recommended for beginners / 推荐新手使用)**

Open `config.yaml` in the project root, find the `api_keys` section, paste your key:

打开项目根目录的 `config.yaml`，找到 `api_keys` 部分，粘贴密钥：

```yaml
api_keys:
  exa: "your-api-key-here"    # Paste your key here / 在这里粘贴你的密钥
```

**Option B: Use `.env` file**

Copy `.env.example` to `.env` and fill in:

```env
EXA_API_KEY=your-api-key-here
```

### Step 3: Install dependencies / 安装依赖

```bash
pip install -r requirements.txt
```

### Step 4: Verify / 验证

```bash
python check_integration.py
```

Expected output / 预期输出:
```
SKILL.md exists
.instructions.md exists
Core modules import successfully
API Key configured
All dependencies installed
All checks passed!
```

### Step 5: Use it! / 开始使用

**In VS Code with Claude:** Press `Ctrl+L`, type your query.

**Command line:**
```bash
python src/claude_skill.py "Apple stock news"
python src/claude_skill.py "Generate report for TSLA" --research
python src/claude_skill.py "AI stocks analysis" --json
```

---

## Configuration Guide / 配置指南

All settings are in one file: **`config.yaml`**. Every option has Chinese + English comments.

所有设置集中在一个文件：**`config.yaml`**。每个选项都有中英文注释。

| Section / 配置项 | What it controls / 控制内容 | Default / 默认值 |
|---|---|---|
| `api_keys.exa` | Exa API key (required) / Exa API 密钥（必填） | `""` |
| `search.type` | Search speed vs quality / 搜索速度与质量 | `"auto"` |
| `search.num_results` | Results per search / 每次搜索结果数 | `10` |
| `validation.min_cross_validation_sources` | Min sources for verification / 交叉验证最少来源数 | `2` |
| `validation.block_export_on_high_risk` | Block export if data unreliable / 数据不可靠时禁止导出 | `true` |
| `source_tiers` | Customize source credibility ranking / 自定义来源可信度排名 | see file |
| `export.markdown_dir` | Markdown output folder / Markdown 输出目录 | `"research Output/markdown"` |
| `export.pdf_dir` | PDF output folder / PDF 输出目录 | `"research Output/pdf"` |
| `network.max_retries` | Retry on network failure / 网络失败重试次数 | `3` |

---

## Features / 功能特性

### Research Frameworks / 研究框架
- **Mature Company** (成熟公司): 7-step methodology with 10-point scoring
- **Growth Company** (成长性公司): 14 sections covering market/team/financials
- **Web3 Project** (Web3 项目): 15 sections including tokenomics/on-chain data

Framework is auto-detected based on your query keywords.

### 10+ Valuation Methods / 10+ 种估值方法
DCF, Graham Formula, PE/PB/PS ratios, EV/EBITDA, PEG, DDM, Owner Earnings, Replacement Cost, with automated cross-validation.

### Data Credibility System / 数据可信度体系

All financial data is validated through a 4-tier source credibility system:

| Tier | Description / 描述 | Examples / 示例 |
|------|---|---|
| Tier 1 | Official/Regulatory (官方/监管) | SEC, FRED, DeFiLlama, Etherscan |
| Tier 2 | Mainstream Financial (主流财经) | Bloomberg, Reuters, Yahoo Finance |
| Tier 3 | Analytical Reference (分析参考) | Investopedia, Zacks, TipRanks |
| Tier 4 | Needs Verification (需验证) | Other sources |

You can customize these tiers in `config.yaml` under `source_tiers`.

### Data Validation / 数据验证
- Cross-validation: critical data verified from 2+ independent sources
- Freshness enforcement: automatic stale data flagging
- Citation audit: scan reports for uncited financial figures
- Hallucination prevention: blocks export if data quality is too low
- Confidence scoring: high / medium / low assessment per data point

### Report Export / 报告导出
- Dual format: Markdown + PDF
- Professional PDF with CJK font support
- Templated file naming
- Pre-export audit enforcement

---

## Project Structure / 项目结构

```
config.yaml              <-- THE ONLY FILE YOU NEED TO EDIT / 你唯一需要编辑的文件
.env                     <-- Alternative: API keys here / 备选：API 密钥放这里

src/
  config.py              <-- Centralized config loader / 统一配置加载器
  claude_skill.py        <-- CLI entry point / 命令行入口

  search/
    exa_searcher.py      <-- Exa API search with retry / Exa 搜索（含重试）

  core/
    researcher.py        <-- Research report generation / 投研报告生成
    valuation.py         <-- 10+ valuation methods / 10+ 估值方法
    freshness.py         <-- Data freshness checker / 数据时效性检查
    validator.py         <-- Cross-validation & scoring / 交叉验证与评分

  server/
    mcp_server.py        <-- MCP protocol server (14 tools) / MCP 服务器 (14 工具)
    skill_router.py      <-- Natural language router / 自然语言路由

  export/
    exporter.py          <-- Markdown + PDF export / 报告导出
    naming.py            <-- File naming conventions / 文件命名规则

  utils/
    helpers.py           <-- Utility functions / 工具函数

  examples/              <-- Example code / 示例代码

config/
  exa_config.json        <-- Exa API settings / Exa API 设置
  mcp_config.json        <-- MCP server settings / MCP 服务器设置

research Output/
  markdown/              <-- Exported .md reports / 导出的 Markdown 报告
  pdf/                   <-- Exported .pdf reports / 导出的 PDF 报告
  templates/             <-- Report templates / 报告模板
```

---

## MCP Tools Available / 可用 MCP 工具

| # | Tool / 工具 | Description / 描述 |
|---|---|---|
| 1 | `search_stock_news` | Search stock news by ticker / 按代码搜索股票新闻 |
| 2 | `search_market_analysis` | Market trend analysis / 市场趋势分析 |
| 3 | `search_company_info` | Company research / 公司研究 |
| 4 | `deep_research` | Thorough deep search / 深度研究搜索 |
| 5 | `generate_research_report` | Generate report skeleton / 生成报告骨架 |
| 6 | `get_research_queries` | Prioritized search queries / 优先搜索查询列表 |
| 7 | `check_report_freshness` | Flag stale data / 标记过期数据 |
| 8 | `check_unfilled_fields` | Find missing fields / 查找未填字段 |
| 9 | `calculate_valuation` | Run valuation methods / 运行估值方法 |
| 10 | `get_position_sizing` | Buy ladder & zones / 建仓阶梯与区域 |
| 11 | `get_do_not_invest_checklist` | Investment discipline rules / 投资纪律清单 |
| 12 | `audit_report_citations` | Detect hallucination risk / 检测幻觉风险 |
| 13 | `export_report` | Export to MD/PDF/both / 导出报告 |
| 14 | `validate_data_point` | Cross-validate data / 交叉验证数据点 |

---

## Usage Examples / 使用示例

### In Claude Chat / 在 Claude 对话中

```
You: Generate a research report for Apple (AAPL)
You: What's the latest with Tesla stock?
You: Calculate DCF valuation for MSFT with FCF=60B, growth=12%
You: Run the do-not-invest checklist for growth company
```

### Python API

```python
from src.search.exa_searcher import StockSearcher
from src.core.researcher import InvestmentResearcher
from src.core.validator import DataValidator

# Search
searcher = StockSearcher()
results = searcher.search_stock_news("AAPL")
print(StockSearcher.format_results(results))

# Research
researcher = InvestmentResearcher()
report = researcher.generate_report_skeleton("Apple", "AAPL", "us")

# Validate
validator = DataValidator()
result = validator.validate_data_point(
    value=38.3, label="Revenue (B)",
    sources=[
        {"name": "SEC 10-Q", "url": "https://sec.gov/...", "date": "2026-03-15", "value": 38.3},
        {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/...", "date": "2026-03-15", "value": 38.2},
    ]
)
print(result["confidence"])  # "high"
```

---

## Data Integrity Rules / 数据完整性规则

1. **No fabricated numbers** - All financial data must come from search results or APIs, never from memory
2. **Source attribution required** - Every data point tagged with `[Source: XX | Date: YYYY-MM-DD]`
3. **Cross-validation mandatory** - Critical data from 2+ independent sources
4. **Freshness enforcement** - Stale data auto-flagged, configurable thresholds
5. **Pre-export audit** - Reports scanned for uncited data before export
6. **Price verification** - Stock prices must be real-time verified from 2+ sources

---

## Troubleshooting / 故障排查

| Problem / 问题 | Solution / 解决方案 |
|---|---|
| `EXA_API_KEY not found` | Set key in `config.yaml` or `.env` / 在 config.yaml 或 .env 中设置密钥 |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` / 运行安装命令 |
| Search timeout | Check internet; increase `network.timeout` in config.yaml / 检查网络；增加超时设置 |
| PDF export fails | Install Chromium: `pip install playwright && playwright install chromium` |
| Encoding errors | Set `PYTHONIOENCODING=utf-8` in environment / 设置环境变量 |

---

## Version / 版本

- **Current**: v0.3.0
- **Python**: >= 3.9
- **Status**: Production Ready

---

## License

See [LICENSE](LICENSE) file.
