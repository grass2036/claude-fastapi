#!/usr/bin/env python3
"""
使用正确的Python环境运行Agent系统
解决CrewAI导入问题的启动脚本
"""

import sys
import os
import subprocess
from pathlib import Path

# 配置正确的Python路径
HOMEBREW_PYTHON = "/opt/homebrew/Cellar/python@3.9/3.9.22/Frameworks/Python.framework/Versions/3.9/bin/python3.9"

def check_python_env():
    """检查Python环境和依赖"""
    print("🔍 检查Python环境...")
    
    # 检查CrewAI安装
    try:
        result = subprocess.run([HOMEBREW_PYTHON, "-m", "pip", "show", "crewai"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ CrewAI已安装")
            print(f"   位置: Homebrew Python 3.9")
            return True
        else:
            print("❌ CrewAI未找到")
            return False
    except Exception as e:
        print(f"❌ 检查CrewAI时出错: {e}")
        return False

def run_agent_example():
    """使用正确的Python环境运行Agent示例"""
    print("\n🤖 使用Agent系统生成文档...")
    
    # Agent代码
    agent_code = '''
import sys
sys.path.append("/Users/chiyingjie/code/git/claude-fastapi/agents")

try:
    from claude_integration import claude_integration
    
    print("✅ Claude集成可用")
    
    # 基础功能测试
    health = claude_integration.health_check()
    print(f"系统状态: {health['status']}")
    
    # 生成文档示例
    print("\\n🔹 生成项目状态文档...")
    docs = claude_integration.generate_documentation(
        "agents/README.md", 
        "api"
    )
    print(f"✅ 文档生成完成: {len(docs)} 字符")
    
    # 尝试CrewAI Agent
    try:
        from doc_agent import doc_agent
        print("\\n🤖 CrewAI Agent可用!")
        
        # 使用Agent生成简单文档
        simple_doc = doc_agent.generate_api_documentation("agents/")
        print(f"✅ Agent文档生成完成")
        
    except Exception as e:
        print(f"⚠️ CrewAI Agent暂不可用: {e}")
        print("   可以继续使用基础Claude集成功能")

except Exception as e:
    print(f"❌ 执行失败: {e}")
    '''
    
    try:
        # 使用Homebrew Python运行
        result = subprocess.run([HOMEBREW_PYTHON, "-c", agent_code], 
                              capture_output=True, text=True, timeout=60)
        
        print("📊 执行结果:")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("警告/错误信息:")
            print(result.stderr)
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("⏰ 执行超时")
        return False
    except Exception as e:
        print(f"❌ 执行异常: {e}")
        return False

def main():
    """主函数"""
    print("🚀 Agent系统配置和测试")
    print("=" * 50)
    
    # 检查环境
    if not check_python_env():
        print("\n💡 建议:")
        print("1. 确保使用Homebrew Python: brew install python@3.9")
        print("2. 重新安装CrewAI: /opt/homebrew/bin/python3.9 -m pip install crewai")
        return
    
    # 运行Agent示例
    success = run_agent_example()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Agent系统配置成功!")
        print("\n📖 使用方式:")
        print("python3.9 agents/run_agent.py")
    else:
        print("⚠️ 部分功能可能需要进一步配置")
        print("基础Claude集成功能应该可用")

if __name__ == "__main__":
    main()