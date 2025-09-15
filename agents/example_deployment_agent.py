"""
部署Agent使用示例和测试用例
演示DeploymentAgent的各种功能和使用场景
"""

import sys
from pathlib import Path

# 添加agents目录到Python路径
sys.path.append(str(Path(__file__).parent))

try:
    from deployment_agent import (
        deployment_agent,
        containerize_app,
        setup_pipeline,
        configure_envs,
        setup_monitoring,
        optimize_performance,
        create_dr_plan,
        check_deployment_health
    )
    from task_coordinator import task_coordinator, TaskType, TaskPriority
    print("✅ 部署Agent模块导入成功")
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    print("💡 请确保CrewAI已安装: pip install crewai")


def demo_containerization():
    """演示容器化功能"""
    print("\n" + "="*60)
    print("🐳 容器化功能演示")
    print("="*60)
    
    # 测试容器化应用
    services = ['backend', 'frontend', 'db', 'redis']
    result = containerize_app(services, environment='production')
    
    print("📋 容器化结果:")
    if result.get('status') == 'success':
        print(f"✅ 状态: {result['status']}")
        print(f"📝 容器化计划: {len(result['containerization_plan'])} 个步骤")
        for step in result['containerization_plan']:
            print(f"   {step}")
        
        print(f"\n🐳 生成的Docker文件: {len(result['docker_files'])} 个")
        for service, dockerfile in result['docker_files'].items():
            print(f"   📄 {service}: 已生成Dockerfile")
        
        print(f"\n📦 Docker Compose配置: 已生成")
        print(f"🎯 优化建议: 已提供")
    else:
        print(f"❌ 容器化失败: {result.get('error', 'Unknown error')}")


def demo_cicd_pipeline():
    """演示CI/CD流水线功能"""
    print("\n" + "="*60)
    print("🚀 CI/CD流水线功能演示")
    print("="*60)
    
    # 测试CI/CD流水线设置
    features = [
        'automated_testing',
        'code_quality', 
        'docker_build',
        'multi_env_deploy',
        'security_scan'
    ]
    result = setup_pipeline(platform='github', features=features)
    
    print("📋 CI/CD流水线设置结果:")
    if result.get('status') == 'success':
        print(f"✅ 状态: {result['status']}")
        print("📝 配置完成:")
        print("   🔧 工作流配置: 已生成")
        print("   ⚙️ 流水线设置: 已完成")
        print("   🎯 部署策略: 已配置")
        print("   🚪 质量门禁: 已启用")
        
        print(f"\n🎯 启用的功能: {len(features)} 个")
        for feature in features:
            print(f"   ✅ {feature}")
    else:
        print(f"❌ 流水线设置失败: {result.get('error', 'Unknown error')}")


def demo_environment_management():
    """演示环境管理功能"""
    print("\n" + "="*60)
    print("🏗️ 环境管理功能演示")
    print("="*60)
    
    # 测试多环境配置
    environments = ['development', 'staging', 'production']
    result = configure_envs(environments)
    
    print("📋 环境配置结果:")
    if result.get('status') == 'success':
        print(f"✅ 状态: {result['status']}")
        print(f"🌍 配置的环境: {len(environments)} 个")
        
        for env in environments:
            print(f"\n📁 {env.upper()} 环境:")
            print("   ✅ 环境配置: 已生成")
            print("   🔐 密钥管理: 已配置")
            print("   ✔️ 配置验证: 已完成")
    else:
        print(f"❌ 环境配置失败: {result.get('error', 'Unknown error')}")


def demo_monitoring_setup():
    """演示监控系统功能"""
    print("\n" + "="*60)
    print("📊 监控系统功能演示")
    print("="*60)
    
    # 测试监控系统设置
    services = ['backend', 'frontend', 'db', 'redis']
    result = setup_monitoring(services, stack='prometheus')
    
    print("📋 监控系统设置结果:")
    if result.get('status') == 'success':
        print(f"✅ 状态: {result['status']}")
        print("📊 监控配置:")
        print("   ✅ Prometheus监控: 已配置")
        print("   📝 日志系统: 已设置")
        print("   🚨 告警规则: 已创建")
        print("   📈 监控仪表板: 已配置")
        
        print(f"\n🎯 监控的服务: {len(services)} 个")
        for service in services:
            print(f"   📊 {service}: 监控已启用")
    else:
        print(f"❌ 监控设置失败: {result.get('error', 'Unknown error')}")


def demo_performance_optimization():
    """演示性能优化功能"""
    print("\n" + "="*60)
    print("⚡ 性能优化功能演示")
    print("="*60)
    
    # 测试性能优化
    optimization_areas = [
        'container_optimization',
        'resource_allocation',
        'caching_strategy',
        'database_tuning'
    ]
    result = optimize_performance('production', optimization_areas)
    
    print("📋 性能优化结果:")
    if result.get('status') == 'success':
        print(f"✅ 状态: {result['status']}")
        print(f"🎯 优化领域: {len(optimization_areas)} 个")
        
        for area in optimization_areas:
            print(f"   ⚡ {area}: 已优化")
        
        print(f"\n📈 监控指标: {len(result['monitoring_metrics'])} 个")
        print("📝 实施步骤: 已制定")
    else:
        print(f"❌ 性能优化失败: {result.get('error', 'Unknown error')}")


def demo_disaster_recovery():
    """演示灾难恢复功能"""
    print("\n" + "="*60)
    print("💾 灾难恢复功能演示")
    print("="*60)
    
    # 测试灾难恢复计划
    services = ['backend', 'db', 'redis']
    objectives = {
        'RTO': '30分钟',  # 恢复时间目标
        'RPO': '5分钟'    # 恢复点目标
    }
    result = create_dr_plan(services, objectives)
    
    print("📋 灾难恢复计划结果:")
    if result.get('status') == 'success':
        print(f"✅ 状态: {result['status']}")
        print("💾 灾难恢复计划:")
        print("   📋 备份策略: 已制定")
        print("   🔧 恢复流程: 已设计")
        print("   🚨 监控告警: 已配置")
        print("   🧪 测试计划: 已制定")
        
        print(f"\n🎯 涵盖的服务: {len(services)} 个")
        for service in services:
            print(f"   💾 {service}: 备份策略已制定")
        
        print(f"\n⏱️ 恢复目标:")
        print(f"   🎯 RTO: {objectives['RTO']}")
        print(f"   📊 RPO: {objectives['RPO']}")
    else:
        print(f"❌ 灾难恢复计划创建失败: {result.get('error', 'Unknown error')}")


def demo_task_coordination():
    """演示任务协调功能"""
    print("\n" + "="*60)
    print("🎯 任务协调功能演示")
    print("="*60)
    
    try:
        # 创建部署相关任务
        tasks = []
        
        # 容器化任务
        task1 = task_coordinator.create_task(
            title="应用容器化",
            description="将FastAPI和Vue.js应用进行容器化部署",
            task_type=TaskType.DEPLOYMENT,
            priority=TaskPriority.HIGH,
            metadata={
                'services': ['backend', 'frontend'],
                'environment': 'production'
            }
        )
        tasks.append(task1)
        
        # CI/CD流水线任务
        task2 = task_coordinator.create_task(
            title="CI/CD流水线设置",
            description="设置GitHub Actions自动化部署流水线",
            task_type=TaskType.DEPLOYMENT,
            priority=TaskPriority.HIGH,
            metadata={
                'platform': 'github',
                'features': ['automated_testing', 'docker_build']
            }
        )
        tasks.append(task2)
        
        # 监控设置任务
        task3 = task_coordinator.create_task(
            title="监控系统配置",
            description="配置Prometheus监控和Grafana仪表板",
            task_type=TaskType.DEPLOYMENT,
            priority=TaskPriority.MEDIUM,
            metadata={
                'services': ['backend', 'frontend'],
                'monitoring_stack': 'prometheus'
            }
        )
        tasks.append(task3)
        
        print("📝 创建的任务:")
        for i, task_id in enumerate(tasks, 1):
            task = task_coordinator.tasks[task_id]
            print(f"   {i}. {task.title} (ID: {task_id[:8]}...)")
            print(f"      状态: {task.status.value}")
            print(f"      优先级: {task.priority.value}")
        
        # 分配和执行任务
        print(f"\n🎯 任务分配和执行:")
        for task_id in tasks:
            assigned = task_coordinator.assign_task(task_id)
            if assigned:
                task = task_coordinator.tasks[task_id]
                print(f"   ✅ 任务 {task.title} 已分配给: {task.assigned_agent}")
                
                # 执行任务
                executed = task_coordinator.execute_task(task_id)
                if executed:
                    print(f"   🚀 任务执行完成")
                else:
                    print(f"   ❌ 任务执行失败")
            else:
                print(f"   ❌ 任务分配失败")
        
        # 显示任务状态
        print(f"\n📊 最终任务状态:")
        for task_id in tasks:
            task = task_coordinator.tasks[task_id]
            print(f"   📋 {task.title}: {task.status.value}")
            if task.result:
                print(f"      结果: {task.result[:100]}...")
                
    except Exception as e:
        print(f"❌ 任务协调演示失败: {e}")


def demo_health_check():
    """演示健康检查功能"""
    print("\n" + "="*60)
    print("🏥 健康检查功能演示")
    print("="*60)
    
    # 检查部署Agent健康状态
    health = check_deployment_health()
    
    print("📋 部署Agent健康检查结果:")
    print(f"🏥 Agent状态: {health.get('agent_status', '未知')}")
    
    # 显示工具状态
    tools_status = health.get('tools_status', {})
    print(f"\n🔧 工具状态: {len(tools_status)} 个工具")
    for tool_name, status in tools_status.items():
        print(f"   {status} {tool_name}")
    
    # 显示能力列表
    capabilities = health.get('capabilities', [])
    print(f"\n💪 Agent能力: {len(capabilities)} 项")
    for capability in capabilities:
        print(f"   {capability}")
    
    # 显示集成状态
    integration_status = health.get('integration_status', {})
    print(f"\n🔗 集成状态:")
    for component, status in integration_status.items():
        print(f"   {status} {component}")


def run_all_demos():
    """运行所有演示"""
    print("🚀 开始DeploymentAgent功能演示")
    print("="*80)
    
    try:
        # 基础功能演示
        demo_containerization()
        demo_cicd_pipeline()
        demo_environment_management()
        demo_monitoring_setup()
        demo_performance_optimization()
        demo_disaster_recovery()
        
        # 高级功能演示
        demo_task_coordination()
        demo_health_check()
        
        print("\n" + "="*80)
        print("✅ 所有DeploymentAgent功能演示完成!")
        print("="*80)
        
        # 总结
        print("\n📊 功能总结:")
        print("🐳 容器化管理: Docker、Docker Compose配置")
        print("🚀 CI/CD流水线: GitHub Actions、质量门禁")
        print("🏗️ 环境管理: 多环境配置、密钥管理")
        print("📊 监控系统: Prometheus、Grafana、告警")
        print("⚡ 性能优化: 容器优化、资源调优")
        print("💾 灾难恢复: 备份策略、恢复流程")
        print("🎯 任务协调: 智能分配、自动执行")
        print("🏥 健康检查: 状态监控、工具验证")
        
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


def interactive_demo():
    """交互式演示菜单"""
    while True:
        print("\n" + "="*60)
        print("🎮 DeploymentAgent 交互式演示")
        print("="*60)
        print("1. 🐳 容器化功能演示")
        print("2. 🚀 CI/CD流水线演示")
        print("3. 🏗️ 环境管理演示")
        print("4. 📊 监控系统演示")
        print("5. ⚡ 性能优化演示")
        print("6. 💾 灾难恢复演示")
        print("7. 🎯 任务协调演示")
        print("8. 🏥 健康检查演示")
        print("9. 🚀 运行全部演示")
        print("0. 🚪 退出")
        
        try:
            choice = input("\n请选择演示项目 (0-9): ").strip()
            
            if choice == "1":
                demo_containerization()
            elif choice == "2":
                demo_cicd_pipeline()
            elif choice == "3":
                demo_environment_management()
            elif choice == "4":
                demo_monitoring_setup()
            elif choice == "5":
                demo_performance_optimization()
            elif choice == "6":
                demo_disaster_recovery()
            elif choice == "7":
                demo_task_coordination()
            elif choice == "8":
                demo_health_check()
            elif choice == "9":
                run_all_demos()
            elif choice == "0":
                print("👋 感谢使用DeploymentAgent演示!")
                break
            else:
                print("❌ 无效选择，请输入0-9之间的数字")
                
        except KeyboardInterrupt:
            print("\n👋 演示已中断，再见!")
            break
        except EOFError:
            print("\n👋 演示结束，再见!")
            break


if __name__ == "__main__":
    print("🎯 DeploymentAgent 使用示例和测试")
    print("选择运行模式:")
    print("1. 运行全部演示")
    print("2. 交互式演示")
    
    try:
        mode = input("请选择模式 (1-2): ").strip()
        
        if mode == "1":
            run_all_demos()
        elif mode == "2":
            interactive_demo()
        else:
            print("默认运行全部演示...")
            run_all_demos()
            
    except (KeyboardInterrupt, EOFError):
        print("\n👋 再见!")
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()