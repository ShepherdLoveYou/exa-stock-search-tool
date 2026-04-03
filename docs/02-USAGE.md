# 📖 完整使用指南

详细的功能使用和输出格式说明。

---

## 🎯 查询类型与检测

### 1. 股票新闻搜索 (Stock News)
**自动检测关键词**: news, latest, developments, update, stock, ticker, AAPL等

```python
queries = [
    "Apple latest news",
    "AAPL stock update", 
    "What's happening with Tesla?",
    "Microsoft recent developments"
]
```

**输出示例**:
```
🔍 Detected: stock_news (confidence: 90.0%)

Stock Ticker: APPLE
Found 3 results
════════════════════════════════════════════════════════════

1. Apple Inc. Stock Analysis
   URL: https://finance.yahoo.com/quote/AAPL/
   Highlight: Apple Inc. (AAPL) Stock Price...
```

---

### 2. 市场分析 (Market Analysis)
**自动检测关键词**: analysis, trend, sector, market, industry, outlook等

```python
queries = [
    "AI stocks market analysis",
    "Sector trends",
    "Tech industry outlook",
    "Market trends for growth stocks"
]
```

**输出示例**:
```json
{
  "search_type": "market_analysis",
  "total_results": 2,
  "results": [
    {
      "title": "AI Stocks 2026 Analysis",
      "url": "https://example.com/...",
      "highlight": "Detailed analysis..."
    }
  ]
}
```

---

### 3. 公司信息查询 (Company Info)
**自动检测关键词**: company, profile, information, earnings, financials, about等

```python
queries = [
    "Microsoft company information",
    "Tesla earnings report",
    "Google financials",
    "Meta company overview"
]
```

---

### 4. 深度研究 (Deep Research)
**自动检测关键词**: research, thorough, detailed, comprehensive, deep dive等

```python
queries = [
    "Deep research on quantum computing",
    "Comprehensive analysis of blockchain",
    "Thorough semiconductor industry study"
]
```

---

## 📊 输出格式

### 文本输出（默认）

```
🔍 Detected: stock_news (confidence: 90.0%)
📝 Query: apple

============================================================
Stock Ticker: APPLE
Found 3 results
============================================================

1. Title: Apple Inc. (AAPL) Stock Price...
   URL: https://finance.yahoo.com/quote/AAPL/
   Highlight: Summary of content...

2. Title: Apple's Latest Earnings Report
   URL: https://example.com/...
   Highlight: Key findings...

3. Title: Apple Stock Analysis
   URL: https://example.com/...
   Highlight: Analysis details...
```

---

### JSON输出（使用 --json）

```json
{
  "query": "apple stock news",
  "search_type": "stock_news",
  "total_results": 3,
  "results": [
    {
      "title": "Apple Inc. (AAPL) Stock Price, News...",
      "url": "https://finance.yahoo.com/quote/AAPL/",
      "highlight": "Apple Inc. (AAPL) Stock Price..."
    },
    {
      "title": "Apple Launches a New iPhone",
      "url": "https://www.fool.com/investing/...",
      "highlight": "Apple's latest product launch..."
    }
  ]
}
```

---

## 💻 使用方法

### 方法1：VS Code Claude Chat
最简单的方式 - Claude自动检测和调用搜索。

```
你: "Tell me about Apple stock"
Claude: [自动搜索] → [返回结果]
```

---

### 方法2：命令行

#### 基础使用
```powershell
.\venv\Scripts\python.exe src/claude_skill.py "query"
```

#### 指定结果数量
```powershell
# 返回5条结果（默认10条）
.\venv\Scripts\python.exe src/claude_skill.py "Apple news" --results 5
```

#### JSON输出
```powershell
# 返回JSON格式
.\venv\Scripts\python.exe src/claude_skill.py "Tesla analysis" --json
```

#### 组合选项
```powershell
# 返回15条结果作为JSON
.\venv\Scripts\python.exe src/claude_skill.py "market trends" --json --results 15
```

---

### 方法3：Python代码

#### 基本搜索
```python
from src.skill_router import ExaSkillRouter

router = ExaSkillRouter()
result = router.search_and_format("Apple stock news")
print(result)
```

#### JSON格式
```python
json_result = router.search_as_json("Tesla market analysis")
print(json_result)
```

#### 直接使用搜索引擎
```python
from src.stock_searcher import StockSearcher

searcher = StockSearcher()

# 股票新闻
news = searcher.search_stock_news("AAPL", num_results=5)

# 市场分析
analysis = searcher.search_market_analysis("AI stocks", num_results=5)

# 公司信息
company = searcher.search_company_info("Microsoft", num_results=5)

# 深度研究
research = searcher.search_with_deep_research("quantum computing", num_results=5)
```

---

## 🔧 命令行参数详解

| 参数 | 说明 | 示例 |
|------|------|------|
| `query` | 搜索查询(必需) | `"Apple news"` |
| `--results N` | 结果数量(默认10) | `--results 5` |
| `--json` | 返回JSON格式 | `--json` |

---

## 🎨 配置选项

### src/stock_searcher.py 中的配置

```python
# 搜索类型 (auto, neural, keyword)
self.search_type = "auto"  # 平衡相关性和速度

# 默认结果数量
self.num_results = 10

# 是否包含内容摘要
include_highlights = True
```

### config/exa_config.json

```json
{
  "search_type": "auto",
  "num_results": 10,
  "highlights": true,
  "max_highlight_length": 4000
}
```

---

## 📝 实际使用例子

### 例子1：查询最新的Apple股票新闻
```powershell
.\venv\Scripts\python.exe src/claude_skill.py "Apple latest stock news" --results 5
```

**结果**: 返回5条最新的Apple股票新闻

---

### 例子2：获取Tesla的市场分析（JSON格式）
```powershell
.\venv\Scripts\python.exe src/claude_skill.py "Tesla market analysis" --json
```

**结果**: 返回JSON格式的市场分析数据

---

### 例子3：深度研究半导体行业
```powershell
.\venv\Scripts\python.exe src/claude_skill.py "semiconductor industry deep research" --results 10
```

**结果**: 返回10条深度研究文章

---

### 例子4：在Claude中自然查询
```
VS Code中按 Ctrl + L 打开Claude Chat

你: "What are the latest developments in AI stocks?"

Claude自动:
1. 识别查询为 "market_analysis" 类型
2. 调用搜索函数
3. 返回最新的AI股票分析结果
```

---

## 🚀 性能参数

| 参数 | 值 | 说明 |
|------|-----|------|
| 平均响应时间 | ~1秒 | Exa自动平衡搜索 |
| 最大结果数 | 无限制 | 根据需要调整 |
| 内容摘要长度 | 4000字符 | 优化token使用 |

---

## ⚡ 优化建议

1. **使用Claude Chat** - 最简便的方式
2. **限制结果数量** - `--results 5` 而不是所有结果
3. **使用JSON** - 当需要编程集成时
4. **缓存结果** - 相同查询不要重复搜索

---

## 📚 更多信息

- [快速开始](01-QUICKSTART.md)
- [Claude集成](03-INTEGRATION.md)
- [API参考](05-API-REFERENCE.md)
- [故障排查](06-TROUBLESHOOTING.md)
