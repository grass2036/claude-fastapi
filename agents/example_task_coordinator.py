#!/usr/bin/env python3
"""
任务协调Agent使用示例
演示如何使用TaskCoordinatorAgent进行智能任务管理
"""

import sys
import os
from pathlib import Path

# 添加agents目录到Python路径
sys.path.append(str(Path(__file__).parent))

from task_coordinator import (
    task_coordinator, 
    handle_request, 
    get_system_status,
    TaskType,
    TaskPriority,
    create_manual_task,
    execute_task_by_id
)


def demo_basic_usage():
    """演示基础使用方法"""
    print("🎯 任务协调Agent - 基础使用示例")
    print("=" * 50)
    
    # 1. 系统状态检查
    print("\n🔹 1. 系统状态检查")
    print("-" * 30)
    status = get_system_status()
    print(f"总任务数: {status['total_tasks']}")
    print(f"队列长度: {status['queue_length']}")
    print(f"系统健康: {status['system_health']['status']}")
    
    # 2. 处理用户请求
    print("\n🔹 2. 处理用户请求")
    print("-" * 30)
    user_request = "为用户管理模块生成API文档和代码分析报告"
    result = handle_request(user_request, auto_execute=True)
    
    print(f"用户请求: {result['request']}")
    print(f"创建任务数: {result['created_tasks']}")
    print(f"任务ID列表: {result['task_ids']}")
    
    if 'execution_results' in result:
        exec_results = result['execution_results']
        print(f"执行结果:")
        print(f"  - 处理任务: {exec_results['processed']}")
        print(f"  - 完成任务: {exec_results['completed']}")
        print(f"  - 失败任务: {exec_results['failed']}")


def demo_manual_task_creation():
    """演示手动任务创建和管理"""
    print("\n🎯 任务协调Agent - 手动任务管理示例")
    print("=" * 50)
    
    # 1. 创建文档生成任务
    print("\n🔹 1. 创建文档生成任务")
    print("-" * 30)
    doc_task_id = create_manual_task(
        title="生成权限中间件API文档",
        description="为backend/middleware/permission.py生成详细的API文档",
        task_type=TaskType.DOCUMENTATION,
        priority=TaskPriority.HIGH
    )
    print(f"文档任务ID: {doc_task_id}")
    
    # 2. 创建代码分析任务
    print("\n🔹 2. 创建代码分析任务")
    print("-" * 30)
    analysis_task_id = create_manual_task(
        title="用户模型代码分析",
        description="分析backend/models/user.py的代码质量和结构",
        task_type=TaskType.CODE_ANALYSIS,
        priority=TaskPriority.MEDIUM
    )
    print(f"分析任务ID: {analysis_task_id}")
    
    # 3. 执行任务
    print("\n🔹 3. 执行任务")
    print("-" * 30)
    
    # 执行文档任务
    print("执行文档生成任务...")
    doc_success = execute_task_by_id(doc_task_id)
    print(f"文档任务执行: {'✅ 成功' if doc_success else '❌ 失败'}")
    
    # 执行分析任务
    print("执行代码分析任务...")
    analysis_success = execute_task_by_id(analysis_task_id)
    print(f"分析任务执行: {'✅ 成功' if analysis_success else '❌ 失败'}")
    
    # 4. 查看任务结果
    print("\n🔹 4. 查看任务结果")
    print("-" * 30)
    
    if doc_success:
        doc_task = task_coordinator.tasks[doc_task_id]
        print(f"文档任务状态: {doc_task.status.value}")
        if doc_task.result:
            print(f"文档结果预览: {doc_task.result[:200]}...")
    
    if analysis_success:
        analysis_task = task_coordinator.tasks[analysis_task_id]
        print(f"分析任务状态: {analysis_task.status.value}")
        if analysis_task.result:
            print(f"分析结果预览: {analysis_task.result[:200]}...")


def demo_complex_workflow():
    """演示复杂工作流处理"""
    print("\n🎯 任务协调Agent - 复杂工作流示例")
    print("=" * 50)
    
    # 模拟复杂的开发需求
    complex_request = """
    我需要为FastAPI项目添加一个新的员工绩效管理功能，包括：
    1. 设计和实现员工绩效评估API
    2. 创建绩效数据模型和数据库迁移
    3. 编写相关的测试用例
    4. 生成完整的API文档
    5. 进行代码质量检查和优化建议
    """
    
    print(f"复杂需求:\n{complex_request}")
    
    # 处理复杂请求
    print("\n🔹 处理复杂工作流...")
    print("-" * 40)
    
    result = handle_request(complex_request, auto_execute=True)
    
    print(f"工作流处理结果:")
    print(f"  - 分解任务数: {result['created_tasks']}")
    print(f"  - 生成任务ID: {len(result['task_ids'])}")
    
    if 'execution_results' in result:
        exec_results = result['execution_results']
        print(f"  - 执行统计:")
        print(f"    * 处理: {exec_results['processed']}")
        print(f"    * 完成: {exec_results['completed']}")
        print(f"    * 失败: {exec_results['failed']}")
        
        # 显示任务详情
        if exec_results['details']:
            print(f"  - 任务详情:")
            for detail in exec_results['details'][:3]:  # 只显示前3个
                print(f"    * {detail['title'][:40]}... - {detail['status']}")


def demo_system_monitoring():
    """演示系统监控功能"""
    print("\n🎯 任务协调Agent - 系统监控示例")
    print("=" * 50)
    
    # 获取详细状态报告
    status_report = get_system_status()
    
    print("\n🔹 系统状态详情")
    print("-" * 30)
    print(f"报告时间: {status_report['timestamp']}")
    print(f"任务统计:")
    for status, count in status_report['task_status'].items():
        print(f"  - {status}: {count}")
    
    print(f"\nAgent状态:")
    for agent_name, agent_status in status_report['agent_status'].items():
        utilization = agent_status['utilization'] * 100
        print(f"  - {agent_name}:")
        print(f"    * 可用: {'✅' if agent_status['available'] else '❌'}")
        print(f"    * 利用率: {utilization:.1f}%")
        print(f"    * 当前任务: {agent_status['current_tasks']}/{agent_status['max_tasks']}")
    
    print(f"\n系统健康:")
    health = status_report['system_health']
    print(f"  - 状态: {health['status']}")
    if 'details' in health:
        # 只显示健康检查的关键信息
        health_lines = health['details'].split('\n')[:5]
        for line in health_lines:
            if line.strip():
                print(f"    {line.strip()}")


def interactive_demo():
    """交互式演示"""
    print("\n🎯 任务协调Agent - 交互式演示")
    print("=" * 50)
    print("输入您的需求，Agent将自动分解并执行任务")
    print("输入 'quit' 退出，输入 'status' 查看系统状态")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n👤 您的需求: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 再见！")
                break
            elif user_input.lower() == 'status':
                demo_system_monitoring()
            elif user_input:
                print(f"\n🤖 处理中...")
                result = handle_request(user_input, auto_execute=True)
                
                print(f"✅ 处理完成:")
                print(f"  - 创建任务: {result['created_tasks']}")
                
                if 'execution_results' in result:
                    exec_results = result['execution_results']
                    print(f"  - 执行结果: 完成{exec_results['completed']}, 失败{exec_results['failed']}")
                    
                    # 显示部分结果
                    for detail in exec_results['details'][:2]:
                        if detail['result']:
                            print(f"  - {detail['title']}: {detail['result'][:100]}...")
            else:
                print("请输入有效的需求")
                
        except KeyboardInterrupt:
            print("\n👋 用户中断，再见！")
            break
        except Exception as e:
            print(f"❌ 处理错误: {e}")


def main():
    """主函数"""
    print("🚀 TaskCoordinatorAgent 使用示例")
    print("=" * 60)
    
    # 运行所有演示
    try:
        demo_basic_usage()
        demo_manual_task_creation()
        demo_complex_workflow()
        demo_system_monitoring()
        
        # 询问是否进入交互模式
        print("\n" + "=" * 60)
        choice = input("是否进入交互式演示？(y/N): ").strip().lower()
        if choice in ['y', 'yes']:
            interactive_demo()
        
    except KeyboardInterrupt:
        print("\n👋 演示中断")
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 显示最终状态
        print("\n🔹 最终系统状态")
        print("-" * 30)
        final_status = get_system_status()
        print(f"总任务数: {final_status['total_tasks']}")
        print(f"完成任务: {final_status['completed_tasks']}")
        print("演示结束！")


if __name__ == "__main__":
    main()