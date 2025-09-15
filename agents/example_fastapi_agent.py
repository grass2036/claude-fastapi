#!/usr/bin/env python3
"""
FastAPI后端开发Agent使用示例
演示如何使用FastAPIBackendAgent进行后端开发任务
"""

import sys
import os
from pathlib import Path

# 添加agents目录到Python路径
sys.path.append(str(Path(__file__).parent))


def demo_basic_fastapi_operations():
    """演示基础FastAPI开发操作"""
    print("🎯 FastAPI后端Agent - 基础操作示例")
    print("=" * 50)
    
    # 由于CrewAI依赖问题，使用简化的示例演示
    print("\n🔹 1. 创建完整资源示例")
    print("-" * 30)
    print("创建Product资源，包含：")
    print("- 数据模型: Product")
    print("- 字段: name(string), price(float), description(text)")
    print("- 包含权限验证: 是")
    print("- 自动生成: Model + Schema + CRUD + API")
    
    # 示例配置
    resource_config = {
        'resource_name': 'products',
        'fields': {
            'name': 'string',
            'price': 'float', 
            'description': 'text',
            'category_id': 'integer',
            'is_active': 'boolean'
        },
        'include_auth': True,
        'custom_endpoints': ['search', 'featured']
    }
    
    print(f"\n配置详情: {resource_config}")
    print("\n✅ 将生成以下文件:")
    print("- backend/models/product.py")
    print("- backend/schemas/product.py") 
    print("- backend/crud/product.py")
    print("- backend/api/v1/products.py")
    
    print("\n🔹 2. 实现单个API端点示例")
    print("-" * 30)
    print("端点配置:")
    print("- 路径: /api/v1/products/search")
    print("- 方法: POST")
    print("- 功能: 商品搜索")
    print("- 权限: 需要登录")
    print("- 请求Schema: ProductSearchRequest")
    print("- 响应Schema: List[ProductResponse]")


def demo_database_design():
    """演示数据库设计功能"""
    print("\n🎯 FastAPI后端Agent - 数据库设计示例")
    print("=" * 50)
    
    print("\n🔹 业务需求分析")
    print("-" * 30)
    requirements = """
    设计一个电商系统的核心数据库：
    
    1. 商品管理
       - 商品基本信息（名称、价格、描述）
       - 商品分类（支持多级分类）
       - 库存管理（数量、预警阈值）
       
    2. 订单管理
       - 订单基本信息
       - 订单项目详情
       - 订单状态流转
       
    3. 用户管理
       - 用户基本信息
       - 用户地址管理
       - 用户偏好设置
    """
    
    print(requirements)
    
    print("\n🔹 数据表设计")
    print("-" * 30)
    tables = [
        'products',
        'categories', 
        'inventory',
        'orders',
        'order_items',
        'users',
        'user_addresses'
    ]
    
    relationships = {
        'products': ['categories', 'inventory'],
        'orders': ['users', 'order_items'],
        'order_items': ['products'],
        'user_addresses': ['users']
    }
    
    print(f"涉及数据表: {tables}")
    print(f"表关系设计: {relationships}")
    
    print("\n✅ 设计输出:")
    print("- ER图描述文档")
    print("- SQLAlchemy模型定义")
    print("- 数据库迁移脚本")
    print("- 索引优化建议")


def demo_authentication_system():
    """演示认证系统实现"""
    print("\n🎯 FastAPI后端Agent - 认证系统示例")
    print("=" * 50)
    
    auth_config = {
        'auth_type': 'JWT',
        'include_rbac': True,
        'oauth_providers': ['Google', 'GitHub'],
        'features': [
            '用户注册登录',
            'JWT令牌管理', 
            '角色权限控制',
            'OAuth第三方登录',
            '密码安全策略',
            '登录失败限制'
        ]
    }
    
    print("\n🔹 认证系统配置")
    print("-" * 30)
    for key, value in auth_config.items():
        if isinstance(value, list):
            print(f"{key}:")
            for item in value:
                print(f"  - {item}")
        else:
            print(f"{key}: {value}")
    
    print("\n✅ 实现组件:")
    print("- JWT编码解码工具")
    print("- 密码哈希验证")
    print("- 权限装饰器")
    print("- 认证中间件")
    print("- OAuth集成")
    print("- 登录API端点")


def demo_performance_optimization():
    """演示性能优化功能"""
    print("\n🎯 FastAPI后端Agent - 性能优化示例")
    print("=" * 50)
    
    print("\n🔹 性能优化目标")
    print("-" * 30)
    optimization_targets = [
        "🚀 响应时间优化 (目标: <200ms)",
        "📈 并发处理提升 (目标: 1000+ QPS)",
        "💾 内存使用优化 (减少50%)",
        "🗃️ 数据库查询优化 (减少N+1查询)",
        "🎯 资源消耗降低 (CPU/内存)"
    ]
    
    for target in optimization_targets:
        print(f"  {target}")
    
    print("\n🔹 优化策略")
    print("-" * 30)
    strategies = {
        '异步处理': 'async/await优化，异步数据库连接',
        '数据库优化': 'Query优化，索引调整，连接池配置',
        '缓存策略': 'Redis缓存，查询结果缓存，静态资源缓存',
        '序列化优化': 'Pydantic优化，JSON序列化加速',
        '中间件调优': '请求处理流程优化，中间件顺序调整'
    }
    
    for strategy, description in strategies.items():
        print(f"  {strategy}: {description}")


def demo_code_review():
    """演示代码审查功能"""
    print("\n🎯 FastAPI后端Agent - 代码审查示例")
    print("=" * 50)
    
    review_files = [
        "backend/api/v1/users.py",
        "backend/models/user.py",
        "backend/crud/user.py",
        "backend/core/security.py"
    ]
    
    print("\n🔹 审查文件列表")
    print("-" * 30)
    for file in review_files:
        print(f"  📄 {file}")
    
    print("\n🔹 审查维度")
    print("-" * 30)
    review_dimensions = [
        "🔍 代码质量检查 - 命名规范、代码结构",
        "🏗️ 架构设计评估 - 模块化、依赖关系",
        "🚀 性能优化建议 - 查询优化、异步处理", 
        "🛡️ 安全性审查 - 权限控制、数据验证",
        "📚 文档完整性 - docstring、注释质量",
        "🧪 测试覆盖度 - 单元测试、集成测试"
    ]
    
    for dimension in review_dimensions:
        print(f"  {dimension}")
    
    print("\n✅ 输出内容:")
    print("- 详细问题分析报告")
    print("- 具体改进建议") 
    print("- 重构代码示例")
    print("- 最佳实践推荐")


def demo_task_coordinator_integration():
    """演示与任务协调器的集成"""
    print("\n🎯 FastAPI后端Agent - 任务协调器集成示例")
    print("=" * 50)
    
    print("\n🔹 使用任务协调器处理复杂需求")
    print("-" * 30)
    
    complex_request = """
    为电商系统实现商品管理功能：
    1. 设计商品数据模型（包含分类、库存）
    2. 实现商品CRUD API接口
    3. 添加商品搜索和筛选功能
    4. 生成完整的API文档
    5. 进行性能优化
    """
    
    print(f"复杂需求:\n{complex_request}")
    
    print("\n🔹 任务分解结果")
    print("-" * 30)
    
    decomposed_tasks = [
        "📋 数据库设计任务 - 设计Product/Category/Inventory模型",
        "🔧 API开发任务 - 实现商品CRUD接口",
        "🔍 搜索功能任务 - 实现商品搜索和筛选",
        "📖 文档生成任务 - 生成API文档",
        "⚡ 性能优化任务 - 优化查询和响应速度"
    ]
    
    for i, task in enumerate(decomposed_tasks, 1):
        print(f"  {i}. {task}")
    
    print("\n✅ 协调器优势:")
    print("- 自动任务分解和分配")
    print("- 多Agent协同工作") 
    print("- 智能依赖管理")
    print("- 进度跟踪监控")


def demo_integration_examples():
    """演示集成使用示例"""
    print("\n🎯 FastAPI后端Agent - 集成使用示例")
    print("=" * 50)
    
    print("\n🔹 完整开发流程")
    print("-" * 30)
    workflow_steps = [
        "1️⃣ 需求分析 → 数据库设计",
        "2️⃣ 数据模型 → SQLAlchemy模型生成",
        "3️⃣ 业务逻辑 → CRUD操作实现",
        "4️⃣ API接口 → FastAPI路由生成",
        "5️⃣ 数据验证 → Pydantic Schema",
        "6️⃣ 权限控制 → JWT认证集成",
        "7️⃣ 文档生成 → API文档输出",
        "8️⃣ 性能优化 → 查询和缓存优化",
        "9️⃣ 代码审查 → 质量检查和重构"
    ]
    
    for step in workflow_steps:
        print(f"  {step}")
    
    print("\n🔹 代码使用示例")
    print("-" * 30)
    code_example = '''
# 使用FastAPI Agent的简化示例

# 1. 创建完整资源
from agents.fastapi_agent import create_resource

result = create_resource(
    resource_name="products",
    fields={
        "name": "string",
        "price": "float", 
        "description": "text"
    },
    include_auth=True
)

# 2. 实现自定义端点
from agents.fastapi_agent import implement_endpoint

endpoint_code = implement_endpoint(
    endpoint_path="/products/search",
    method="POST",
    description="商品搜索接口",
    include_auth=True
)

# 3. 设计数据库
from agents.fastapi_agent import design_database

schema_design = design_database(
    requirements="电商商品管理系统",
    tables=["products", "categories"],
    relationships={"products": ["categories"]}
)
'''
    
    print(code_example)


def interactive_demo():
    """交互式演示"""
    print("\n🎯 FastAPI后端Agent - 交互式演示")
    print("=" * 50)
    print("选择要演示的功能：")
    print("1. 创建资源 (resource)")
    print("2. 数据库设计 (database)")
    print("3. 认证系统 (auth)")
    print("4. 性能优化 (performance)")
    print("5. 代码审查 (review)")
    print("6. 任务协调器 (coordinator)")
    print("7. 所有演示 (all)")
    print("输入 'quit' 退出")
    print("-" * 50)
    
    while True:
        try:
            choice = input("\n👤 请选择功能 (1-7 或 all): ").strip().lower()
            
            if choice in ['quit', 'exit', 'q']:
                print("👋 演示结束！")
                break
            elif choice in ['1', 'resource']:
                demo_basic_fastapi_operations()
            elif choice in ['2', 'database']:
                demo_database_design()
            elif choice in ['3', 'auth']:
                demo_authentication_system()
            elif choice in ['4', 'performance']:
                demo_performance_optimization()
            elif choice in ['5', 'review']:
                demo_code_review()
            elif choice in ['6', 'coordinator']:
                demo_task_coordinator_integration()
            elif choice in ['7', 'all']:
                demo_basic_fastapi_operations()
                demo_database_design()
                demo_authentication_system()
                demo_performance_optimization()
                demo_code_review()
                demo_task_coordinator_integration()
                demo_integration_examples()
            else:
                print("❌ 无效选择，请输入 1-7 或 all")
                
        except KeyboardInterrupt:
            print("\n👋 演示中断！")
            break
        except Exception as e:
            print(f"❌ 演示错误: {e}")


def main():
    """主函数"""
    print("🚀 FastAPIBackendAgent 使用示例")
    print("=" * 60)
    print("FastAPI后端开发专家Agent演示")
    print("包含完整的后端开发工作流示例")
    print("=" * 60)
    
    try:
        # 运行默认演示
        demo_basic_fastapi_operations()
        demo_database_design()
        demo_authentication_system()
        demo_performance_optimization()
        demo_code_review()
        demo_task_coordinator_integration()
        demo_integration_examples()
        
        # 询问是否进入交互模式
        print("\n" + "=" * 60)
        choice = input("是否进入交互式演示？(y/N): ").strip().lower()
        if choice in ['y', 'yes']:
            interactive_demo()
        
        print("\n✅ FastAPI Agent演示完成！")
        print("🎯 功能特点:")
        print("  - 完整的FastAPI开发工作流")
        print("  - 智能代码生成和优化")
        print("  - 数据库设计和建模")
        print("  - 认证和权限系统")
        print("  - 性能优化和代码审查")
        print("  - 与任务协调器无缝集成")
        
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()