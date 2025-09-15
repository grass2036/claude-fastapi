#!/bin/bash
# Agent系统项目级安装脚本

echo "🚀 设置Agent系统项目环境"
echo "================================"

# 检查是否在项目根目录
if [ ! -f "CLAUDE.md" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

echo "📦 创建项目虚拟环境..."

# 创建虚拟环境（如果不存在）
if [ ! -d "venv-agents" ]; then
    python3 -m venv venv-agents
    echo "✅ 虚拟环境已创建: venv-agents/"
else
    echo "⚠️ 虚拟环境已存在: venv-agents/"
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv-agents/bin/activate

# 更新pip
echo "📥 更新pip..."
pip install --upgrade pip

# 安装主项目依赖
echo "📦 安装主项目依赖..."
pip install -r requirements.txt

# 安装Agent系统依赖
echo "🤖 安装Agent系统依赖..."

# 尝试安装兼容版本的CrewAI
echo "尝试安装CrewAI..."

# 方法1：尝试最新版本
pip install crewai --quiet 2>/dev/null && echo "✅ CrewAI最新版本安装成功" || {
    echo "⚠️ 最新版本失败，尝试兼容版本..."
    
    # 方法2：尝试指定版本
    pip install "crewai==0.30.0" --quiet 2>/dev/null && echo "✅ CrewAI v0.30.0安装成功" || {
        echo "⚠️ v0.30.0失败，尝试更早版本..."
        
        # 方法3：尝试更早期版本
        pip install "crewai==0.28.0" --quiet 2>/dev/null && echo "✅ CrewAI v0.28.0安装成功" || {
            echo "❌ CrewAI安装失败，仅使用基础Claude集成功能"
        }
    }
}

# 安装其他必要依赖
pip install pydantic python-dotenv

echo ""
echo "🧪 测试Agent系统..."

# 测试基础功能
python -c "
import sys
sys.path.append('agents')
try:
    from claude_integration import claude_integration
    health = claude_integration.health_check()
    print('✅ Claude集成功能正常')
    print('   状态:', health['status'])
    print('   Python文件:', health.get('python_files_count', 0), '个')
except Exception as e:
    print('❌ 基础功能异常:', e)

try:
    import crewai
    print('✅ CrewAI可用 (版本:', crewai.__version__, ')')
except Exception as e:
    print('⚠️ CrewAI不可用:', str(e)[:50], '...')
    print('   可继续使用基础Claude集成功能')
"

echo ""
echo "================================"
echo "🎉 Agent系统环境配置完成！"
echo ""
echo "📖 使用方法:"
echo "1. 激活环境: source venv-agents/bin/activate"  
echo "2. 运行示例: python agents/example.py"
echo "3. 退出环境: deactivate"
echo ""
echo "📁 环境位置: $(pwd)/venv-agents/"
echo "🔧 配置文件: agents/.env"