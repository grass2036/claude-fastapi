# 🤖 Agent开发系统

> 🎯 基于Claude Code和CrewAI的多专业Agent开发团队

## 📋 概述

这是一个专门为FastAPI + Vue.js项目设计的智能Agent系统，包含文档生成和前端开发两个专业Agent，能够自动化各种开发任务。

### ✨ 主要功能

#### 📖 **文档生成Agent**
- 📋 **API文档生成** - 自动生成FastAPI接口文档
- 🏗️ **技术文档** - 深入的架构和实现文档  
- 👥 **用户指南** - 面向最终用户的操作手册
- 📄 **README生成** - 项目介绍和快速开始指南
- 🔍 **代码分析** - 智能代码结构和质量分析

#### 🎨 **前端开发专家Agent**
- ⚡ **Vue组件生成** - 基于需求自动生成Vue 3 + Vuetify组件
- 🎯 **UI设计** - Material Design 3.0规范的界面设计
- 📱 **响应式布局** - 移动端优先的响应式设计方案
- ♿ **用户体验优化** - 可访问性和性能优化建议
- 📚 **组件库** - 可复用组件库设计和实现

## 🚀 快速开始

### 1. 安装依赖

```bash
# 基础版本（仅Claude Code集成）
cd agents && python setup.py

# 完整版本（包含CrewAI Agent）
pip install crewai[tools] pydantic python-dotenv
```

### 2. 基础使用

```python
# 不依赖CrewAI的基础用法
from agents.claude_integration import claude_integration

# 系统健康检查
health = claude_integration.health_check()
print(health['status'])

# 生成API文档
api_docs = claude_integration.generate_documentation(
    "backend/middleware/permission.py", 
    "api"
)
print(api_docs)

# 代码分析
analysis = claude_integration.analyze_file("backend/models/user.py")
print(analysis)
```

### 3. Agent使用（需要CrewAI）

```python
# 文档生成Agent
from agents.doc_agent import generate_api_docs, generate_tech_docs

# 生成权限中间件API文档
api_docs = generate_api_docs("backend/middleware/permission.py")
print(api_docs)

# 生成技术架构文档
tech_docs = generate_tech_docs("权限中间件系统")
print(tech_docs)

# 前端开发Agent
from agents.frontend_agent import generate_vue_component, design_ui_layout

# 生成Vue组件
component = generate_vue_component(
    "UserCard",
    "用户信息展示卡片，包含头像、姓名、部门等信息"
)

# 设计UI页面布局
layout = design_ui_layout(
    "用户管理页面",
    "需要用户列表、搜索、筛选、批量操作等功能"
)
```

### 4. Agent管理器使用

```python
from agents.manager import agent_manager

# 列出所有可用Agent
agents = agent_manager.list_agents()
print(f"可用Agent: {agents}")

# 使用统一接口调用Agent
result = agent_manager.execute_task(
    'frontend', 
    'generate_component',
    component_name='ProductCard',
    requirements='商品展示卡片组件'
)

# 获取系统状态
status = agent_manager.system_status()
print(status)
```

## 📚 详细使用指南

### 🔧 基础工具类

#### ClaudeCodeIntegration
```python
from agents.claude_integration import claude_integration

# 分析项目结构
structure = claude_integration.get_project_structure()

# 代码质量审查
review = claude_integration.review_code("backend/api/v1/users.py")

# 改进建议
suggestions = claude_integration.suggest_improvements("用户管理模块")

# 列出Python文件
files = claude_integration.list_python_files()
```

### 🤖 Agent系统

#### 文档生成Agent
```python
from agents.doc_agent import doc_agent

# API文档
api_result = doc_agent.generate_api_documentation("backend/middleware")

# 技术文档  
tech_result = doc_agent.generate_technical_documentation("权限系统")

# 用户指南
user_result = doc_agent.generate_user_guide("权限管理功能")

# README文档
readme_result = doc_agent.generate_readme("FastAPI项目")

# 代码分析 + 文档生成
analysis_result = doc_agent.analyze_and_document("backend/models")
```

## 🎯 使用场景

### 场景1: 为新功能生成文档
```python
# 为权限中间件生成完整文档
from agents.doc_agent import generate_api_docs, generate_tech_docs

# 1. API接口文档
api_docs = generate_api_docs("backend/middleware/permission.py")

# 2. 技术实现文档
tech_docs = generate_tech_docs("权限中间件")

# 3. 保存到文件
with open("docs/permission_api.md", "w") as f:
    f.write(api_docs)
```

### 场景2: 代码质量检查
```python
from agents.claude_integration import claude_integration

# 检查关键文件
critical_files = [
    "backend/middleware/permission.py",
    "backend/api/v1/users.py",
    "backend/models/user.py"
]

for file_path in critical_files:
    print(f"\n🔍 检查: {file_path}")
    review = claude_integration.review_code(file_path)
    print(review)
```

### 场景3: 项目文档梳理
```python
from agents.doc_agent import generate_readme, analyze_and_document

# 1. 更新项目README
readme = generate_readme("项目概述")

# 2. 生成模块文档
modules = ["backend/middleware", "backend/api", "backend/models"]
for module in modules:
    docs = analyze_and_document(module)
    # 保存文档...
```

## ⚙️ 配置选项

### 环境变量配置

创建 `agents/.env` 文件：

```bash
# 项目设置
PROJECT_PATH="/Users/chiyingjie/code/git/claude-fastapi"

# Agent设置
AGENT_VERBOSE=true
AGENT_MAX_ITER=3
AGENT_TIMEOUT=300

# Claude Code设置
CLAUDE_AUTO_ACCEPT=true
CLAUDE_TIMEOUT=300

# 成本控制
DAILY_API_BUDGET=10
MAX_TOKENS_PER_REQUEST=2000
```

### Agent自定义配置

```python
from agents.doc_agent import DocumentationAgent

# 创建自定义Agent
custom_agent = DocumentationAgent()

# 修改Agent属性
custom_agent.agent.verbose = False
custom_agent.agent.max_iter = 5
```

## 🧪 测试和示例

### 运行示例
```bash
# 运行交互式示例
cd agents && python example.py

# 运行安装和健康检查
python setup.py
```

### 示例输出
```
🚀 文档生成Agent示例
==================================================

🔹 示例1: 基础用法
========================================
1. 系统健康检查...
   状态: ✅ 正常

2. 生成项目结构文档...
   ✅ 项目结构分析完成
   预览: 📁 项目结构分析:

## FastAPI项目结构

```
claude-fastapi/
├── backend/          # 后端代码
│   ├── middleware/   # 中间件
│   ├── api/         # API路由
│   ├── models/      # 数据模型
│   └── ...
├── frontend/        # 前端代码
└── ...
```

3. 分析权限中间件...
   ✅ 权限中间件分析完成
```

## 💡 最佳实践

### 1. 成本控制
```python
# 设置预算限制
import os
os.environ['DAILY_API_BUDGET'] = '10'  # 每日$10限制

# 批量操作时使用缓存
claude_integration.enable_cache = True
```

### 2. 质量保证
```python
# 总是先运行健康检查
health = claude_integration.health_check()
if health['status'] != "✅ 正常":
    print("系统异常，请检查配置")
    exit(1)

# 分批处理大型项目
files = claude_integration.list_python_files()
for batch in [files[i:i+5] for i in range(0, len(files), 5)]:
    # 处理一批文件
    process_file_batch(batch)
```

### 3. 文档管理
```python
# 建立文档版本控制
import datetime

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
doc_file = f"docs/api_docs_{timestamp}.md"

with open(doc_file, "w") as f:
    f.write(api_docs)
```

## ❗ 注意事项

### 系统要求
- ✅ Python 3.8+
- ✅ Claude Code CLI 已安装
- ✅ 项目路径可访问
- ✅ 网络连接正常

### 已知限制
- ⚠️ 每次API调用有成本
- ⚠️ 大文件分析可能较慢
- ⚠️ 需要稳定的网络连接
- ⚠️ Agent输出需要人工review

### 故障排除
```python
# 检查Claude Code
import subprocess
result = subprocess.run(["claude", "--version"], capture_output=True)
print(f"Claude Code状态: {result.returncode == 0}")

# 检查项目路径
from pathlib import Path
project_path = Path("/Users/chiyingjie/code/git/claude-fastapi")
print(f"项目路径存在: {project_path.exists()}")

# 检查Python文件
files = list(project_path.rglob("*.py"))
print(f"Python文件数量: {len(files)}")
```

## 🔮 后续计划

- [ ] 添加更多Agent角色（代码审查、测试生成）
- [ ] 支持更多文档格式（HTML、PDF）
- [ ] 集成CI/CD流程
- [ ] Web界面支持
- [ ] 多语言文档生成

## 📞 支持

如有问题或建议，请：
1. 检查本文档的故障排除部分
2. 运行 `python setup.py` 进行系统诊断
3. 查看日志文件 `agents/logs/agent.log`

---

**版本**: 1.0.0  
**更新时间**: 2025-09-15  
**兼容性**: Claude Code + FastAPI 项目