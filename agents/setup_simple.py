#!/usr/bin/env python3
"""
简化的Agent系统配置脚本
专注于基础功能，避免复杂的CrewAI配置
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """设置基础环境"""
    print("🔧 配置Agent系统环境...")
    
    # 确保日志目录存在
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    print(f"✅ 日志目录: {logs_dir.absolute()}")
    
    # 检查配置文件
    env_file = Path(".env")
    if env_file.exists():
        print(f"✅ 配置文件: {env_file.absolute()}")
    else:
        print("⚠️ 配置文件不存在，请检查 .env 文件")
    
    return True

def test_basic_functions():
    """测试基础功能"""
    print("\n🧪 测试基础功能...")
    
    try:
        from claude_integration import claude_integration
        
        # 健康检查
        health = claude_integration.health_check()
        print(f"✅ 健康检查: {health['status']}")
        
        # 项目结构
        structure = claude_integration.get_project_structure()
        print(f"✅ 项目结构分析: {len(structure)} 字符")
        
        # Python文件列表
        files = claude_integration.list_python_files()
        print(f"✅ Python文件扫描: {len(files)} 个文件")
        
        return True
        
    except Exception as e:
        print(f"❌ 基础功能测试失败: {e}")
        return False

def test_crewai_agent():
    """测试CrewAI Agent (可选)"""
    print("\n🤖 测试CrewAI Agent...")
    
    try:
        import crewai
        print(f"✅ CrewAI可用 (版本: {crewai.__version__})")
        
        # 尝试导入我们的Agent
        from doc_agent import doc_agent
        print("✅ 文档Agent导入成功")
        
        return True
        
    except ImportError as e:
        print(f"⚠️ CrewAI不可用: {e}")
        print("   建议使用基础Claude集成功能")
        return False
    except Exception as e:
        print(f"❌ Agent测试失败: {e}")
        return False

def create_usage_example():
    """创建使用示例"""
    example_code = '''# Agent系统使用示例

## 基础用法 (总是可用)
```python
from claude_integration import claude_integration

# 健康检查
health = claude_integration.health_check()
print(health['status'])

# 分析文件
analysis = claude_integration.analyze_file("backend/models/user.py")
print(analysis)

# 生成文档
docs = claude_integration.generate_documentation("backend/api/v1/users.py", "api")
print(docs)
```

## 高级Agent用法 (需要CrewAI)
```python
try:
    from doc_agent import generate_api_docs, generate_tech_docs
    
    # API文档
    api_docs = generate_api_docs("backend/middleware/permission.py")
    
    # 技术文档
    tech_docs = generate_tech_docs("权限中间件系统")
    
except ImportError:
    print("CrewAI Agent不可用，使用基础功能")
```

## 推荐的启动命令
```bash
# 使用Homebrew Python (推荐)
/opt/homebrew/Cellar/python@3.9/3.9.22/Frameworks/Python.framework/Versions/3.9/bin/python3.9

# 或者设置别名
alias py39='/opt/homebrew/Cellar/python@3.9/3.9.22/Frameworks/Python.framework/Versions/3.9/bin/python3.9'
py39 agents/example.py
```
'''
    
    with open("USAGE.md", "w", encoding="utf-8") as f:
        f.write(example_code)
    
    print(f"✅ 使用示例已创建: {Path('USAGE.md').absolute()}")

def main():
    """主函数"""
    print("🚀 Agent系统简化配置")
    print("=" * 40)
    
    # 设置环境
    setup_environment()
    
    # 测试基础功能
    basic_ok = test_basic_functions()
    
    # 测试Agent功能
    agent_ok = test_crewai_agent()
    
    # 创建使用示例
    create_usage_example()
    
    print("\n" + "=" * 40)
    print("📊 配置结果:")
    print(f"✅ 基础Claude集成: {'可用' if basic_ok else '不可用'}")
    print(f"{'✅' if agent_ok else '⚠️'} CrewAI Agent: {'可用' if agent_ok else '不可用(可选)'}")
    
    if basic_ok:
        print("\n🎉 Agent系统配置完成!")
        print("📖 查看 USAGE.md 了解详细使用方法")
    else:
        print("\n❌ 配置失败，请检查环境设置")

if __name__ == "__main__":
    main()