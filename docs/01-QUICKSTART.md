# ⚡ 快速开始指南 (5分钟)

**最快的方式开启您的搜索系统。**

---

## 🚀 方式1：VS Code Claude Chat（推荐）

### 3个步骤就能开始

#### 1️⃣ 打开项目
```
快捷键: Ctrl + K, Ctrl + O
选择: d:\MCP project\EXA search MCP
点击: Select Folder
```
等待加载完成（≈ 5秒）

#### 2️⃣ 打开Claude Chat
```
快捷键: Ctrl + L
```

#### 3️⃣ 输入查询
```
"Apple最新股票新闻？"
"Tesla市场分析"
"科技股现在怎么样？"
```
✅ Claude自动调用搜索！

---

## 🖥️ 方式2：命令行使用

### 基础查询
```powershell
.\venv\Scripts\python.exe src/claude_skill.py "Your query here"
```

### 高级选项
```powershell
# JSON格式输出
--json

# 限制结果数量（默认10条）
--results 5

# 组合使用
.\venv\Scripts\python.exe src/claude_skill.py "Apple news" --json --results 3
```

### 实际例子
```powershell
# 查询股票新闻
.\venv\Scripts\python.exe src/claude_skill.py "Apple stock news" --results 5

# 获取市场分析
.\venv\Scripts\python.exe src/claude_skill.py "AI stocks market analysis" --json
```

---

## 🐍 方式3：Python代码

```python
from src.skill_router import ExaSkillRouter

router = ExaSkillRouter()

# 文本格式结果
result = router.search_and_format("Apple news")
print(result)

# JSON格式结果
json_result = router.search_as_json("Tesla analysis")
print(json_result)
```

---

## ✅ 验证系统

```powershell
# 检查所有依赖
.\venv\Scripts\python.exe check_integration.py

# 运行演示
.\venv\Scripts\python.exe -m src.examples.claude_skill_demo
```

---

## 🎯 支持的查询类型

| 类型 | 示例 | 检测准确率 |
|-----|------|---------|
| 股票新闻 | "Apple news", "AAPL update" | 90% |
| 市场分析 | "AI stocks analysis" | 85% |
| 公司信息 | "Microsoft company profile" | 80% |
| 深度研究 | "semiconductor industry research" | 75% |

---

## 🆘 常见问题

**Q: 出现编码错误？**
```powershell
$env:PYTHONIOENCODING="utf-8"
.\venv\Scripts\python.exe src/claude_skill.py "query"
```

**Q: API密钥找不到？**
检查 `.env` 文件：
```
EXA_API_KEY=your-key-here
```

**Q: 模块导入错误？**
```powershell
.\venv\Scripts\pip.exe install -r requirements.txt
```

---

## 📚 下一步

- [完整使用指南](02-USAGE.md)
- [Claude集成详情](03-INTEGRATION.md)
- [部署指南](04-DEPLOYMENT.md)
- [故障排查](06-TROUBLESHOOTING.md)

**准备好了？现在就在VS Code中按 `Ctrl + L` 开始吧！** 🚀
