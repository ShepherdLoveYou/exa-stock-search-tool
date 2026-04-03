# 🔌 API 参考文档

完整的函数、类和参数说明。

---

## 📦 模块结构

```
src/
├── stock_searcher.py      # 核心搜索类
├── skill_router.py        # 智能路由
├── claude_skill.py        # Claude接口
└── examples/              # 示例代码
```

---

## 🔍 StockSearcher 类

位置: `src/stock_searcher.py`

### 初始化

```python
from src.stock_searcher import StockSearcher

searcher = StockSearcher(api_key=None)
```

**参数**:
- `api_key` (str, optional) - Exa API Key。如果为None，从.env读取

**异常**:
- `ValueError` - 如果API Key未找到

---

### 方法：search_stock_news()

搜索特定股票的新闻。

```python
result = searcher.search_stock_news(
    ticker="AAPL",
    num_results=10,
    include_highlights=True
)
```

**参数**:
- `ticker` (str) - 股票代码，如"AAPL", "GOOGL"
- `num_results` (int, optional) - 返回结果数量，默认10
- `include_highlights` (bool, optional) - 是否包含内容摘要，默认True

**返回**: `Dict`
```python
{
    "ticker": "AAPL",
    "query": "AAPL news",
    "total_results": 10,
    "results": [
        {
            "title": "...",
            "url": "...",
            "highlight": "..."
        }
    ]
}
```

---

### 方法：search_market_analysis()

搜索市场分析和行业趋势。

```python
result = searcher.search_market_analysis(
    topic="AI stocks",
    num_results=10,
    include_highlights=True
)
```

**参数**:
- `topic` (str) - 分析主题，如"AI stocks", "tech sector"
- `num_results` (int, optional) - 返回结果数量，默认10
- `include_highlights` (bool, optional) - 是否包含内容摘要，默认True

**返回**: `Dict` (format同search_stock_news)

---

### 方法：search_company_info()

搜索公司信息和财务数据。

```python
result = searcher.search_company_info(
    company_name="Microsoft",
    num_results=10,
    include_highlights=True
)
```

**参数**:
- `company_name` (str) - 公司名称
- `num_results` (int, optional) - 返回结果数量，默认10
- `include_highlights` (bool, optional) - 是否包含内容摘要，默认True

**返回**: `Dict`

---

### 方法：search_with_deep_research()

执行深度研究和详细分析。

```python
result = searcher.search_with_deep_research(
    query="quantum computing",
    num_results=10,
    include_highlights=True
)
```

**参数**:
- `query` (str) - 研究查询
- `num_results` (int, optional) - 返回结果数量，默认10
- `include_highlights` (bool, optional) - 是否包含内容摘要，默认True

**返回**: `Dict`

---

### 静态方法：format_results()

格式化搜索结果为可读的文本。

```python
formatted = StockSearcher.format_results(
    results=result_dict,
    max_items=5
)
```

**参数**:
- `results` (Dict) - 搜索结果字典
- `max_items` (int, optional) - 最多显示的结果数，默认所有结果

**返回**: `str` - 格式化的文本

---

## 🧭 ExaSkillRouter 类

位置: `src/skill_router.py`

### 初始化

```python
from src.skill_router import ExaSkillRouter

router = ExaSkillRouter(api_key=None)
```

**参数**:
- `api_key` (str, optional) - Exa API Key

---

### 方法：detect_search_type()

检测查询类型并返回搜索类型和置信度。

```python
search_type, confidence = router.detect_search_type(
    query="Apple latest news"
)
```

**参数**:
- `query` (str) - 用户查询

**返回**: `Tuple[str, float]`
- search_type: `"stock_news"`, `"market_analysis"`, `"company_info"`, `"deep_research"`, 或 `"unknown"`
- confidence: 置信度 (0.0-100.0)

**示例**:
```python
>>> router.detect_search_type("Apple latest news")
("stock_news", 90.0)

>>> router.detect_search_type("Market analysis")
("market_analysis", 85.0)
```

---

### 方法：search()

执行智能路由搜索。

```python
result = router.search(
    query="Apple stock news",
    num_results=10
)
```

**参数**:
- `query` (str) - 搜索查询
- `num_results` (int, optional) - 返回结果数量，默认10

**返回**: `Dict` - 搜索结果

---

### 方法：search_and_format()

执行搜索并返回格式化的文本。

```python
formatted_text = router.search_and_format(
    query="Apple stock news",
    num_results=10
)
print(formatted_text)
```

**参数**:
- `query` (str) - 搜索查询
- `num_results` (int, optional) - 返回结果数量，默认10

**返回**: `str` - 格式化的文本结果

**输出示例**:
```
🔍 Detected: stock_news (confidence: 90.0%)
📝 Query: apple

============================================================
Stock Ticker: APPLE
Found 3 results
============================================================

1. Title: Apple Inc. (AAPL) Stock Price...
   URL: https://finance.yahoo.com/quote/AAPL/
   Highlight: Summary...
```

---

### 方法：search_as_json()

执行搜索并返回JSON格式。

```python
json_result = router.search_as_json(
    query="Tesla market analysis",
    num_results=10
)
import json
print(json.dumps(json_result, indent=2))
```

**参数**:
- `query` (str) - 搜索查询
- `num_results` (int, optional) - 返回结果数量，默认10

**返回**: `Dict` - JSON格式的结果

**JSON结构**:
```json
{
  "query": "tesla market analysis",
  "search_type": "market_analysis",
  "confidence": 85.0,
  "total_results": 10,
  "results": [
    {
      "title": "...",
      "url": "...",
      "highlight": "..."
    }
  ]
}
```

---

## 🎯 Claude Skill 函数

位置: `src/claude_skill.py`

### 函数：search_stock()

Claude可调用的搜索函数。

```python
def search_stock(query: str, num_results: int = 10) -> str
```

**参数**:
- `query` (str) - 搜索查询
- `num_results` (int, optional) - 返回结果数量，默认10

**返回**: `str` - 格式化的文本结果

**说明**: 这是Claude Chat会自动调用的函数

---

### 函数：search_stock_json()

Claude可调用的JSON搜索函数。

```python
def search_stock_json(query: str, num_results: int = 10) -> dict
```

**参数**:
- `query` (str) - 搜索查询
- `num_results` (int, optional) - 返回结果数量，默认10

**返回**: `dict` - JSON格式的结果

---

## 📊 数据结构

### 搜索结果格式

```python
{
    "ticker": "AAPL",           # 股票代码
    "query": "AAPL news",       # 搜索查询
    "total_results": 10,        # 结果总数
    "results": [
        {
            "title": "Apple Inc. (AAPL) Stock Price...",
            "url": "https://finance.yahoo.com/quote/AAPL/",
            "highlight": "Apple Inc. (AAPL) Stock Price...",
            "published_date": "2024-04-01"  # 可选
        },
        ...
    ]
}
```

### 路由结果格式

```python
{
    "search_type": "stock_news",           # 检测到的类型
    "confidence": 90.0,                    # 置信度 (0-100)
    "query": "apple news",
    "total_results": 10,
    "results": [...]
}
```

---

## 🔧 配置参数

### Exa API 配置

```python
# 在 config/exa_config.json 中
{
    "search_type": "auto",          # 搜索类型: auto, neural, keyword
    "num_results": 10,              # 默认结果数
    "highlights": true,             # 是否包含摘要
    "max_highlight_length": 4000,   # 摘要最大字符数
    "timeout": 30                   # 超时时间（秒）
}
```

### Exa搜索类型

| 类型 | 说明 | 响应时间 |
|------|------|--------|
| auto | 平衡相关性和速度 | ~1秒 |
| neural | 神经网络搜索，更精确 | ~2秒 |
| keyword | 关键词搜索，更快 | ~0.5秒 |

---

## 💡 使用示例

### 例子1：基础搜索

```python
from src.stock_searcher import StockSearcher

searcher = StockSearcher()
result = searcher.search_stock_news("AAPL", num_results=5)
print(result)
```

---

### 例子2：智能路由

```python
from src.skill_router import ExaSkillRouter

router = ExaSkillRouter()

# 自动检测类型
search_type, confidence = router.detect_search_type("Apple news")
print(f"Type: {search_type}, Confidence: {confidence}%")

# 执行搜索
result = router.search("Apple news", num_results=5)
```

---

### 例子3：获取格式化文本

```python
from src.skill_router import ExaSkillRouter

router = ExaSkillRouter()
formatted = router.search_and_format("Tesla market analysis")
print(formatted)
```

---

### 例子4：JSON输出

```python
from src.skill_router import ExaSkillRouter
import json

router = ExaSkillRouter()
result = router.search_as_json("Microsoft company info")
print(json.dumps(result, indent=2))
```

---

### 例子5：命令行使用

```powershell
# 基础查询
.\venv\Scripts\python.exe src/claude_skill.py "Apple news"

# 指定结果数量
.\venv\Scripts\python.exe src/claude_skill.py "Tesla analysis" --results 5

# JSON输出
.\venv\Scripts\python.exe src/claude_skill.py "market trends" --json

# 组合选项
.\venv\Scripts\python.exe src/claude_skill.py "AI stocks" --json --results 20
```

---

## 🔄 查询类型检测

### 自动检测规则

| 查询类型 | 关键词模式 | 置信度 |
|---------|----------|------|
| stock_news | news, latest, update, ticker, AAPL, TSLA... | 90% |
| market_analysis | analysis, trend, sector, market, industry... | 85% |
| company_info | company, profile, info, earnings, financials... | 80% |
| deep_research | research, thorough, detailed, comprehensive... | 75% |

---

## ⚡ 性能优化

### 响应时间

- **Exa API**: ~1秒 (auto mode)
- **路由检测**: <50ms
- **格式化**: <100ms
- **总计**: ~1.2秒

### Token优化

- 使用摘要模式：最多4000字符
- 限制结果数量：默认10条
- JSON压缩：最小化数据大小

---

## 🆘 错误处理

### 常见异常

```python
try:
    result = searcher.search_stock_news("AAPL")
except ValueError as e:
    print(f"API Key错误: {e}")
except Exception as e:
    print(f"搜索错误: {e}")
```

---

## 📚 更多资源

- [快速开始](01-QUICKSTART.md)
- [完整使用](02-USAGE.md)
- [Claude集成](03-INTEGRATION.md)
- [项目结构](07-PROJECT-STRUCTURE.md)
