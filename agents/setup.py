"""
Agent系统安装和配置脚本
"""

import subprocess
import sys
import os
from pathlib import Path


def install_dependencies():
    """安装必要的依赖"""
    print("🔧 安装Agent系统依赖...")
    
    dependencies = [
        "crewai[tools]",
        "pydantic>=2.0.0",
        "python-dotenv"
    ]
    
    for dep in dependencies:
        print(f"安装 {dep}...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", dep],
                check=True,
                capture_output=True
            )
            print(f"✅ {dep} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ {dep} 安装失败: {e}")
            return False
    
    return True


def check_claude_code():
    """检查Claude Code是否可用"""
    print("🔍 检查Claude Code...")
    
    try:
        result = subprocess.run(
            ["claude", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"✅ Claude Code可用: {result.stdout.strip()}")
            return True
        else:
            print("❌ Claude Code不可用")
            return False
            
    except FileNotFoundError:
        print("❌ Claude Code未安装")
        print("请先安装Claude Code: https://claude.ai/code")
        return False
    except Exception as e:
        print(f"❌ 检查Claude Code时出错: {e}")
        return False


def create_config_file():
    """创建配置文件"""
    print("📝 创建配置文件...")
    
    config_content = """# Agent系统配置文件

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

# 日志设置
LOG_LEVEL=INFO
LOG_FILE="agents/logs/agent.log"
"""
    
    config_path = Path("agents/.env")
    config_path.parent.mkdir(exist_ok=True)
    
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print(f"✅ 配置文件已创建: {config_path}")


def create_logs_directory():
    """创建日志目录"""
    logs_dir = Path("agents/logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ 日志目录已创建: {logs_dir}")


def run_health_check():
    """运行健康检查"""
    print("🔍 运行系统健康检查...")
    
    try:
        # 导入并运行健康检查
        sys.path.append(str(Path(__file__).parent))
        from claude_integration import claude_integration
        
        health_status = claude_integration.health_check()
        
        print("\n📊 健康检查报告:")
        print(f"Claude Code: {'✅' if health_status['claude_available'] else '❌'}")
        print(f"项目路径: {'✅' if health_status['project_exists'] else '❌'}")
        print(f"Python文件: {health_status.get('python_files_count', 0)}个")
        print(f"总体状态: {health_status['status']}")
        
        return health_status['status'] == "✅ 正常"
        
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False


def main():
    """主安装流程"""
    print("🚀 开始安装Agent系统...")
    print("=" * 50)
    
    steps = [
        ("安装依赖", install_dependencies),
        ("检查Claude Code", check_claude_code),
        ("创建配置文件", create_config_file),
        ("创建日志目录", create_logs_directory),
        ("健康检查", run_health_check)
    ]
    
    success_count = 0
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        try:
            if step_func():
                success_count += 1
                print(f"✅ {step_name}完成")
            else:
                print(f"❌ {step_name}失败")
        except Exception as e:
            print(f"❌ {step_name}异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 安装完成: {success_count}/{len(steps)} 步骤成功")
    
    if success_count == len(steps):
        print("\n🎉 Agent系统安装成功！")
        print("\n📖 快速开始:")
        print("```python")
        print("from agents.doc_agent import generate_api_docs")
        print("result = generate_api_docs('backend/middleware/permission.py')")
        print("print(result)")
        print("```")
    else:
        print("\n⚠️ 安装未完全成功，请检查上述错误信息")


if __name__ == "__main__":
    main()