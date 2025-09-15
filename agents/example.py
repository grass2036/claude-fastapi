"""
Agent系统使用示例
演示如何使用文档生成Agent和前端开发Agent
"""

import os
import sys
from pathlib import Path

# 添加路径以便导入
sys.path.append(str(Path(__file__).parent))

def example_1_basic_usage():
    """示例1: 基础用法 - 不依赖CrewAI"""
    print("🔹 示例1: 基础用法")
    print("=" * 40)
    
    try:
        from claude_integration import claude_integration
        
        # 检查系统状态
        print("1. 系统健康检查...")
        health = claude_integration.health_check()
        print(f"   状态: {health['status']}")
        
        # 生成项目结构文档
        print("\n2. 生成项目结构文档...")
        structure = claude_integration.get_project_structure()
        print("   ✅ 项目结构分析完成")
        print(f"   预览: {structure[:200]}...")
        
        # 分析权限中间件
        print("\n3. 分析权限中间件...")
        analysis = claude_integration.analyze_file("backend/middleware/permission.py")
        print("   ✅ 权限中间件分析完成")
        print(f"   预览: {analysis[:200]}...")
        
        # 生成API文档
        print("\n4. 生成权限中间件API文档...")
        api_docs = claude_integration.generate_documentation(
            "backend/middleware/permission.py", 
            "api"
        )
        print("   ✅ API文档生成完成")
        print(f"   预览: {api_docs[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 示例执行失败: {e}")
        return False


def example_2_advanced_usage():
    """示例2: 高级用法 - 使用CrewAI Agent"""
    print("\n🔹 示例2: Agent用法")
    print("=" * 40)
    
    try:
        # 检查CrewAI是否可用
        try:
            import crewai
            print("   ✅ CrewAI可用")
        except ImportError:
            print("   ⚠️ CrewAI未安装，跳过Agent示例")
            print("   安装命令: pip install crewai[tools]")
            return False
        
        from doc_agent import doc_agent
        
        # 使用Agent生成技术文档
        print("1. 使用Agent生成权限中间件技术文档...")
        tech_docs = doc_agent.generate_technical_documentation(
            "backend/middleware/permission.py"
        )
        print("   ✅ 技术文档生成完成")
        print(f"   预览: {str(tech_docs)[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Agent示例执行失败: {e}")
        return False


def example_3_batch_documentation():
    """示例3: 批量文档生成"""
    print("\n🔹 示例3: 批量文档生成")
    print("=" * 40)
    
    try:
        from claude_integration import claude_integration
        
        # 获取所有Python文件
        python_files = claude_integration.list_python_files()
        print(f"1. 发现 {len(python_files)} 个Python文件")
        
        # 重点关注的文件
        priority_files = [
            "backend/middleware/permission.py",
            "backend/middleware/session.py", 
            "backend/api/v1/users.py",
            "backend/models/user.py"
        ]
        
        print("2. 生成重点文件的文档...")
        docs_generated = 0
        
        for file_path in priority_files:
            if file_path in python_files:
                try:
                    print(f"   📝 处理: {file_path}")
                    docs = claude_integration.generate_documentation(file_path, "api")
                    docs_generated += 1
                    print(f"   ✅ 完成: {len(docs)} 字符")
                except Exception as e:
                    print(f"   ❌ 失败: {e}")
        
        print(f"\n3. 批量生成完成: {docs_generated}/{len(priority_files)} 个文件")
        return True
        
    except Exception as e:
        print(f"   ❌ 批量生成失败: {e}")
        return False


def example_4_interactive_mode():
    """示例4: 交互式文档生成"""
    print("\n🔹 示例4: 交互式模式")
    print("=" * 40)
    
    try:
        from claude_integration import claude_integration
        
        print("交互式文档生成器")
        print("输入 'help' 查看命令，输入 'quit' 退出")
        
        while True:
            command = input("\n📝 doc> ").strip().lower()
            
            if command == 'quit':
                break
            elif command == 'help':
                print("""
可用命令:
- health: 系统健康检查
- structure: 项目结构分析
- list: 列出Python文件
- analyze <file>: 分析指定文件
- docs <file>: 生成文档
- quit: 退出
                """)
            elif command == 'health':
                health = claude_integration.health_check()
                print(f"系统状态: {health['status']}")
            elif command == 'structure':
                structure = claude_integration.get_project_structure()
                print(structure[:500] + "..." if len(structure) > 500 else structure)
            elif command == 'list':
                files = claude_integration.list_python_files()
                for i, file in enumerate(files[:10], 1):
                    print(f"{i:2d}. {file}")
                if len(files) > 10:
                    print(f"... 还有 {len(files) - 10} 个文件")
            elif command.startswith('analyze '):
                file_path = command[8:].strip()
                analysis = claude_integration.analyze_file(file_path)
                print(analysis[:500] + "..." if len(analysis) > 500 else analysis)
            elif command.startswith('docs '):
                file_path = command[5:].strip()
                docs = claude_integration.generate_documentation(file_path)
                print(docs[:500] + "..." if len(docs) > 500 else docs)
            else:
                print("未知命令，输入 'help' 查看帮助")
        
        return True
        
    except KeyboardInterrupt:
        print("\n👋 交互模式已退出")
        return True
    except Exception as e:
        print(f"❌ 交互模式失败: {e}")
        return False


def example_5_frontend_agent():
    """示例5: 前端开发Agent"""
    print("\n🔹 示例5: 前端开发Agent")
    print("=" * 40)
    
    try:
        from manager import agent_manager
        
        print("1. 检查前端Agent状态...")
        frontend_agent = agent_manager.get_agent('frontend')
        if not frontend_agent:
            print("   ❌ 前端Agent不可用")
            return False
        
        print("   ✅ 前端Agent可用")
        
        # 获取Agent能力
        print("\n2. 查看前端Agent能力...")
        capabilities = agent_manager.get_agent_capabilities('frontend')
        for agent_name, tasks in capabilities.items():
            print(f"   {agent_name}: {', '.join(tasks)}")
        
        # 生成Vue组件示例
        print("\n3. 生成Vue组件示例...")
        try:
            component_result = agent_manager.execute_task(
                'frontend', 
                'generate_component',
                component_name='UserCard',
                requirements='用户信息展示卡片组件，包含头像、姓名、部门信息，支持点击查看详情'
            )
            print("   ✅ Vue组件生成完成")
            print(f"   预览: {str(component_result)[:200]}...")
        except Exception as e:
            print(f"   ❌ 组件生成失败: {e}")
        
        # 设计UI布局示例
        print("\n4. 设计UI布局示例...")
        try:
            layout_result = agent_manager.execute_task(
                'frontend',
                'design_layout', 
                page_name='用户管理页面',
                business_requirements='需要展示用户列表、搜索筛选、批量操作、用户详情等功能'
            )
            print("   ✅ UI布局设计完成")
            print(f"   预览: {str(layout_result)[:200]}...")
        except Exception as e:
            print(f"   ❌ 布局设计失败: {e}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 前端Agent示例失败: {e}")
        return False


def example_6_agent_manager():
    """示例6: Agent管理器统一调用"""
    print("\n🔹 示例6: Agent管理器")
    print("=" * 40)
    
    try:
        from manager import agent_manager
        
        # 列出所有可用Agent
        print("1. 列出所有可用Agent...")
        agents = agent_manager.list_agents()
        print(f"   可用Agent: {', '.join(agents)}")
        
        # 获取系统状态
        print("\n2. 获取系统状态...")
        status = agent_manager.system_status()
        for agent_name, agent_status in status.items():
            status_icon = "✅" if agent_status['status'] == 'healthy' else "❌"
            print(f"   {status_icon} {agent_name}: {agent_status['status']}")
        
        # 获取所有Agent能力
        print("\n3. 获取所有Agent能力...")
        all_capabilities = agent_manager.get_agent_capabilities()
        for agent_name, tasks in all_capabilities.items():
            print(f"   🤖 {agent_name}:")
            for task in tasks:
                print(f"      - {task}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Agent管理器示例失败: {e}")
        return False


def main():
    """主函数"""
    print("🚀 Agent系统示例")
    print("=" * 50)
    
    examples = [
        ("基础用法", example_1_basic_usage),
        ("Agent用法", example_2_advanced_usage), 
        ("批量生成", example_3_batch_documentation),
        ("前端Agent", example_5_frontend_agent),
        ("Agent管理器", example_6_agent_manager),
    ]
    
    success_count = 0
    
    for name, example_func in examples:
        try:
            if example_func():
                success_count += 1
        except Exception as e:
            print(f"❌ {name}示例失败: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 示例完成: {success_count}/{len(examples)} 个成功")
    
    # 询问是否进入交互模式
    if success_count > 0:
        try:
            choice = input("\n是否进入交互模式? (y/N): ").strip().lower()
            if choice in ['y', 'yes']:
                example_4_interactive_mode()
        except KeyboardInterrupt:
            pass
    
    print("\n👋 示例结束")


if __name__ == "__main__":
    main()