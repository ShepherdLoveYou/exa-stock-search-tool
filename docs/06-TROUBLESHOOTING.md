# 🆘 故障排查指南

常见问题的解决方案。

---

## 🔴 错误排查

### 错误1：UnicodeEncodeError

**现象**:
```
UnicodeEncodeError: 'gbk' codec can't encode character '\u274c'
```

**原因**: Windows PowerShell默认编码不支持UTF-8

**解决方案**:
```powershell
# 设置环境变量
$env:PYTHONIOENCODING="utf-8"

# 然后运行命令
.\venv\Scripts\python.exe src/claude_skill.py "query"
```

**持久化方案**:
在PowerShell配置文件中添加：
```powershell
$env:PYTHONIOENCODING="utf-8"
```

---

### 错误2：API Key未找到

**现象**:
```
ValueError: EXA_API_KEY not found
```

**原因**: .env文件中缺少API Key或文件不存在

**解决方案**:

1. **检查.env文件是否存在**
```powershell
Test-Path .env
```

2. **如果不存在，复制.env.example**
```powershell
cp .env.example .env
```

3. **编辑.env并添加API Key**
```powershell
notepad .env
```

4. **在文件中添加**
```
EXA_API_KEY=your-actual-api-key-here
```

5. **保存并重启终端**

---

### 错误3：Module导入失败

**现象**:
```
ModuleNotFoundError: No module named 'exa_py'
```

**原因**: 依赖未安装或虚拟环境未激活

**解决方案**:

1. **确认虚拟环境激活**
```powershell
# 检查提示符是否显示 (venv)
# 如果没有，运行：
.\venv\Scripts\Activate.ps1
```

2. **重新安装依赖**
```powershell
pip install -r requirements.txt
```

3. **验证安装**
```powershell
pip list | grep exa_py
```

---

### 错误4：Python不在PATH中

**现象**:
```
'python' is not recognized as an internal or external command
```

**原因**: Python未添加到系统PATH

**解决方案**:

1. **使用完整路径**
```powershell
C:\Users\YourUser\AppData\Local\Programs\Python\Python313\python.exe src/claude_skill.py "query"
```

2. **或重新安装Python**
   - 下载https://www.python.org/
   - 安装时勾选 "Add Python to PATH"
   - 重启VS Code和PowerShell

---

### 错误5：虚拟环境激活失败

**现象**:
```
PowerShell execution policies do not allow scripts to run
```

**原因**: PowerShell执行策略限制

**解决方案**:
```powershell
# 允许当前用户运行脚本
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 然后激活虚拟环境
.\venv\Scripts\Activate.ps1
```

---

### 错误6：Exa API错误

**现象**:
```
exa_py.APIError: Unauthorized
```

**原因**: API Key无效或已过期

**解决方案**:
1. 检查API Key是否正确复制
2. 访问https://dashboard.exa.ai/api-keys 生成新的Key
3. 更新.env文件
4. 重启终端

---

## ⚠️ 常见问题

### Q1: Claude无法获得搜索结果

**症状**: Claude Chat中输入查询后没有返回搜索结果

**检查清单**:
- [ ] SKILL.md文件存在且有效
- [ ] .instructions.md文件存在
- [ ] Claude Chat已从侧栏打开
- [ ] API Key已配置
- [ ] 依赖已安装

**解决步骤**:
```powershell
# 1. 验证集成
python check_integration.py

# 2. 测试命令行
.\venv\Scripts\python.exe src/claude_skill.py "test query"

# 3. 重启Claude Chat
# Ctrl + Shift + L 或关闭并重新打开
```

---

### Q2: 搜索结果不准确

**症状**: 返回的结果与查询不相关

**原因**: 查询表述不清或路由检测失败

**改进方案**:
```
❌ 不好: "Apple"
✅ 更好: "Apple stock news"

❌ 不好: "STOCK"
✅ 更好: "Tesla latest stock news"

❌ 不好: "market"
✅ 更好: "AI semiconductor market analysis"
```

---

### Q3: 响应速度很慢

**症状**: 搜索花费超过5秒

**检查**:
1. 网络连接是否正常
2. Exa API是否响应（通常<1秒）
3. 是否同时进行多个查询

**优化**:
```powershell
# 减少结果数量
.\venv\Scripts\python.exe src/claude_skill.py "query" --results 3

# 避免深度研究查询
# 深度研究查询通常更慢
```

---

### Q4: Claude不识别Skill

**症状**: Claude Chat中没有看到搜索建议

**排查**:
```powershell
# 检查SKILL.md
Test-Path SKILL.md

# 检查.instructions.md
Test-Path .instructions.md

# 查看文件内容
cat SKILL.md | Select-Object -First 10
```

**解决**:
```powershell
# 重新创建文件
# 参考docs文件夹中的templates

# 或重启VS Code
# Ctrl + Shift + P -> Reload Window
```

---

### Q5: 某些查询无法路由

**症状**: 查询被识别为"unknown"类型

**例子**:
```
查询: "stock"
结果: search_type="unknown", confidence=0%
```

**分析**:
- 查询过于简洁
- 缺少足够的上下文关键词

**改进**:
```
❌ "stock"
✅ "stock market news"

❌ "crypto"
✅ "cryptocurrency market analysis"
```

---

## 🔧 调试技巧

### 启用详细输出

```python
from src.skill_router import ExaSkillRouter

router = ExaSkillRouter()

# 检查路由检测
search_type, confidence = router.detect_search_type("your query")
print(f"类型: {search_type}")
print(f"置信度: {confidence}%")

# 执行搜索
result = router.search("your query")
print(f"结果数量: {len(result['results'])}")
```

---

### 测试单个组件

```python
# 测试StockSearcher
from src.stock_searcher import StockSearcher
searcher = StockSearcher()
result = searcher.search_stock_news("AAPL", num_results=3)
print(result)

# 测试ExaSkillRouter
from src.skill_router import ExaSkillRouter
router = ExaSkillRouter()
result = router.search_and_format("Apple news")
print(result)
```

---

### 查看日志

```powershell
# 运行命令并保存输出到文件
.\venv\Scripts\python.exe src/claude_skill.py "query" 2>&1 | Tee-Object -FilePath debug.log

# 查看日志
Get-Content debug.log
```

---

## 🔍 诊断工具

### 集成检查脚本

```powershell
python check_integration.py
```

**输出**:
```
✅ SKILL.md exists
✅ .instructions.md exists
✅ Core modules import successfully
✅ API Key configured (da2769fe-...)
✅ All dependencies installed
✅ All checks passed!
```

---

### 演示程序

```powershell
# 基础演示
python -m src.examples.basic_search

# 完整演示
python -m src.examples.claude_skill_demo

# OpenAI演示
python -m src.examples.openai_function_calling

# Anthropic演示
python -m src.examples.anthropic_tool_use
```

---

## 📋 完整故障排查流程

### 第1步：验证环境

```powershell
# 检查Python
python --version

# 检查虚拟环境
.\venv\Scripts\python.exe --version

# 检查集成
python check_integration.py
```

### 第2步：测试命令行

```powershell
.\venv\Scripts\python.exe src/claude_skill.py "Apple news" --results 3
```

### 第3步：测试Claude Chat

```
打开VS Code
按 Ctrl + L
输入: "Apple latest news"
查看是否返回结果
```

### 第4步：查看日志

```powershell
# 启用详细输出
$env:PYTHONIOENCODING="utf-8"
.\venv\Scripts\python.exe src/claude_skill.py "test" > output.log 2>&1
Get-Content output.log
```

---

## 🤝 获取帮助

如果以上解决方案都不能解决问题：

1. **检查所有配置文件**
   - `.env` - API Key
   - `config/exa_config.json` - 搜索配置
   - `requirements.txt` - 依赖

2. **运行完整诊断**
   ```powershell
   python check_integration.py
   python -m src.examples.claude_skill_demo
   ```

3. **查看错误堆栈**
   ```powershell
   .\venv\Scripts\python.exe -u src/claude_skill.py "query" 2>&1
   ```

4. **参考文档**
   - [快速开始](01-QUICKSTART.md)
   - [部署指南](04-DEPLOYMENT.md)
   - [API参考](05-API-REFERENCE.md)

---

## ✅ 常见解决方案总结

| 问题 | 快速解决 |
|------|--------|
| 编码错误 | `$env:PYTHONIOENCODING="utf-8"` |
| API Key未找到 | 检查`.env`文件 |
| 模块未找到 | 运行`pip install -r requirements.txt` |
| 虚拟环境失败 | 运行`.\venv\Scripts\Activate.ps1` |
| Claude无结果 | 运行`python check_integration.py` |

---

## 📚 相关文档

- [快速开始](01-QUICKSTART.md)
- [部署指南](04-DEPLOYMENT.md)
- [API参考](05-API-REFERENCE.md)
- [完整使用](02-USAGE.md)
