"""
FastAPI后端开发专家Agent
专门负责FastAPI应用开发、数据库设计、API构建等后端任务
"""

from crewai import Agent, Task, Crew, Process
from typing import Dict, List, Any, Optional
from .fastapi_tools import (
    APIGenerationTool,
    ModelGenerationTool,
    CRUDGenerationTool,
    SchemaGenerationTool,
    MigrationGenerationTool
)
from .tools import (
    CodeAnalysisTool,
    ProjectStructureTool,
    HealthCheckTool
)


class FastAPIBackendAgent:
    """FastAPI后端开发专家Agent类"""
    
    def __init__(self):
        # FastAPI专用工具集
        self.fastapi_tools = [
            APIGenerationTool(),
            ModelGenerationTool(),
            CRUDGenerationTool(),
            SchemaGenerationTool(),
            MigrationGenerationTool()
        ]
        
        # 通用开发工具
        self.general_tools = [
            CodeAnalysisTool(),
            ProjectStructureTool(),
            HealthCheckTool()
        ]
        
        # 合并所有工具
        self.tools = self.fastapi_tools + self.general_tools
        
        # 创建专家Agent
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """创建FastAPI后端开发专家Agent"""
        return Agent(
            role='FastAPI Backend Development Expert',
            goal='构建高质量、可扩展的FastAPI后端应用，包括API设计、数据库建模、权限控制和性能优化',
            backstory="""
            你是一位资深的FastAPI后端开发专家，拥有深厚的Python Web开发经验。
            你的专业技能涵盖：
            
            🐍 **Python & FastAPI 专长**:
            - FastAPI框架深度应用和最佳实践
            - 异步编程和高性能API设计
            - Pydantic数据验证和序列化
            - SQLAlchemy ORM和数据库设计
            - Alembic数据库迁移管理
            
            🏗️ **架构设计能力**:
            - RESTful API设计规范
            - 微服务架构和模块化设计
            - 数据库Schema设计和优化
            - 依赖注入和中间件开发
            - 错误处理和异常管理
            
            🔐 **安全与认证**:
            - JWT令牌认证机制
            - RBAC权限控制系统
            - 数据加密和安全最佳实践
            - CORS和安全中间件配置
            - OAuth2和第三方登录集成
            
            📊 **数据库专长**:
            - PostgreSQL高级特性应用
            - Redis缓存策略和实现
            - 数据库查询优化
            - 事务管理和数据一致性
            - 数据库连接池和性能调优
            
            🚀 **DevOps与部署**:
            - Docker容器化部署
            - CI/CD流程设计
            - 监控和日志管理
            - API文档生成和维护
            - 性能测试和负载优化
            
            💡 **开发理念**:
            - 代码清洁度和可维护性
            - 测试驱动开发(TDD)
            - 敏捷开发和持续集成
            - 文档驱动开发
            - 安全第一的开发思维
            
            你的目标是帮助团队构建出高质量、可扩展、安全可靠的FastAPI后端系统。
            """,
            tools=self.tools,
            verbose=True,
            allow_delegation=False,
            max_iter=5
        )
    
    def create_complete_resource(
        self, 
        resource_name: str, 
        fields: Dict[str, str],
        include_auth: bool = True,
        custom_endpoints: List[str] = []
    ) -> Dict[str, str]:
        """创建完整的资源（模型+CRUD+API+Schema）"""
        
        model_name = resource_name.title().rstrip('s')
        table_name = resource_name.lower()
        
        task_description = f"""
        为 {resource_name} 创建完整的FastAPI资源实现，包括：
        
        **资源信息**：
        - 资源名称: {resource_name}
        - 模型名称: {model_name}
        - 数据表名: {table_name}
        - 字段定义: {fields}
        - 包含权限验证: {include_auth}
        - 自定义端点: {custom_endpoints}
        
        **实施步骤**：
        1. 🗃️ 创建SQLAlchemy数据模型
        2. 📋 生成Pydantic验证Schema
        3. 🔧 实现CRUD操作类
        4. 🛣️ 生成FastAPI路由文件
        5. 📝 创建数据库迁移文件
        
        **技术要求**：
        - 遵循FastAPI最佳实践
        - 包含完整的类型注解
        - 实现适当的错误处理
        - 添加详细的文档字符串
        - {'集成JWT权限验证' if include_auth else '无需权限验证'}
        - 生成完整的API文档
        
        **代码质量标准**：
        - 代码清晰可读
        - 遵循PEP 8规范
        - 包含适当的注释
        - 实现数据验证
        - 错误信息友好
        """
        
        task = Task(
            description=task_description,
            agent=self.agent,
            expected_output="完整的FastAPI资源实现，包含所有必要的文件和代码"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        try:
            result = crew.kickoff()
            return {
                'status': 'success',
                'resource_name': resource_name,
                'model_name': model_name,
                'result': result
            }
        except Exception as e:
            return {
                'status': 'error',
                'resource_name': resource_name,
                'error': str(e)
            }
    
    def implement_api_endpoint(
        self, 
        endpoint_path: str, 
        method: str, 
        description: str,
        include_auth: bool = True,
        request_schema: Optional[str] = None,
        response_schema: Optional[str] = None
    ) -> str:
        """实现单个API端点"""
        
        task_description = f"""
        实现FastAPI端点：{method.upper()} {endpoint_path}
        
        **端点需求**：
        - 路径: {endpoint_path}
        - 方法: {method.upper()}
        - 功能描述: {description}
        - 权限验证: {'是' if include_auth else '否'}
        - 请求Schema: {request_schema or '无'}
        - 响应Schema: {response_schema or '标准响应'}
        
        **实现要求**：
        1. 编写完整的端点函数
        2. 添加适当的类型注解
        3. 实现请求数据验证
        4. 添加错误处理逻辑
        5. 编写详细的API文档
        6. {'集成权限中间件' if include_auth else '无需权限验证'}
        
        **代码标准**：
        - 遵循FastAPI规范
        - 包含完整的docstring
        - 实现适当的状态码
        - 返回标准JSON响应
        """
        
        task = Task(
            description=task_description,
            agent=self.agent,
            expected_output="完整的FastAPI端点实现代码"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def design_database_schema(
        self, 
        requirements: str,
        tables: List[str] = [],
        relationships: Dict[str, List[str]] = {}
    ) -> str:
        """设计数据库Schema"""
        
        task_description = f"""
        根据业务需求设计数据库Schema：
        
        **业务需求**：
        {requirements}
        
        **涉及数据表**：
        {tables if tables else '待分析确定'}
        
        **表关系**：
        {relationships if relationships else '待设计'}
        
        **设计任务**：
        1. 🔍 分析业务需求
        2. 📋 识别核心实体和属性
        3. 🔗 设计表间关系
        4. ⚡ 优化数据库性能
        5. 🛡️ 考虑数据安全性
        6. 📝 生成创建脚本
        
        **设计原则**：
        - 遵循数据库设计规范
        - 考虑数据完整性
        - 优化查询性能
        - 支持数据扩展
        - 实现合理的索引策略
        
        **输出内容**：
        - 数据库ER图描述
        - SQLAlchemy模型定义
        - 数据库迁移脚本
        - 关系说明文档
        """
        
        task = Task(
            description=task_description,
            agent=self.agent,
            expected_output="完整的数据库Schema设计方案"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def optimize_api_performance(self, target_api: str) -> str:
        """优化API性能"""
        
        task_description = f"""
        优化FastAPI应用性能，重点关注：{target_api}
        
        **性能优化目标**：
        1. 🚀 提升响应速度
        2. 📈 增加并发处理能力
        3. 💾 优化内存使用
        4. 🗃️ 改进数据库查询效率
        5. 🎯 减少资源消耗
        
        **优化策略**：
        - 异步处理优化
        - 数据库查询优化
        - 缓存策略实施
        - 数据序列化优化
        - 中间件性能调优
        - 连接池配置优化
        
        **分析维度**：
        - 请求响应时间
        - 数据库查询分析
        - 内存使用情况
        - CPU消耗模式
        - 网络传输效率
        
        **实施计划**：
        1. 性能基准测试
        2. 瓶颈识别分析
        3. 优化方案设计
        4. 代码实施改进
        5. 效果验证测试
        """
        
        task = Task(
            description=task_description,
            agent=self.agent,
            expected_output="详细的API性能优化方案和实施代码"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def implement_authentication_system(
        self, 
        auth_type: str = "JWT",
        include_rbac: bool = True,
        oauth_providers: List[str] = []
    ) -> str:
        """实现认证系统"""
        
        task_description = f"""
        实现FastAPI认证和权限系统：
        
        **认证配置**：
        - 认证类型: {auth_type}
        - 包含RBAC: {'是' if include_rbac else '否'}
        - OAuth提供商: {oauth_providers if oauth_providers else '无'}
        
        **系统功能**：
        1. 🔐 用户注册和登录
        2. 🎫 JWT令牌管理
        3. 🔒 密码加密存储
        4. 👥 角色权限管理
        5. 🛡️ API访问控制
        6. 📱 令牌刷新机制
        
        **技术实现**：
        - JWT编码和解码
        - 密码哈希和验证
        - 权限装饰器开发
        - 中间件集成
        - Session管理
        - CORS配置
        
        **安全特性**：
        - 令牌过期管理
        - 刷新令牌机制
        - 密码复杂度验证
        - 登录失败限制
        - 安全头部设置
        
        **集成要求**：
        - 与现有用户模型集成
        - 支持数据库权限存储
        - 提供权限验证装饰器
        - 实现登录登出API
        """
        
        task = Task(
            description=task_description,
            agent=self.agent,
            expected_output="完整的认证和权限系统实现"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def code_review_and_refactor(self, target_files: List[str]) -> str:
        """代码审查和重构"""
        
        task_description = f"""
        对FastAPI代码进行专业审查和重构：
        
        **审查文件**：
        {chr(10).join(f'- {file}' for file in target_files)}
        
        **审查维度**：
        1. 🔍 代码质量检查
        2. 🏗️ 架构设计评估
        3. 🚀 性能优化建议
        4. 🛡️ 安全性审查
        5. 📚 文档完整性
        6. 🧪 测试覆盖度
        
        **重构方向**：
        - 代码结构优化
        - 函数复杂度降低
        - 重复代码消除
        - 命名规范统一
        - 错误处理改进
        - 类型注解完善
        
        **FastAPI特定检查**：
        - 路由设计合理性
        - 依赖注入使用
        - 中间件配置
        - Schema设计优化
        - 异步操作正确性
        - 文档生成质量
        
        **输出要求**：
        - 详细的问题分析
        - 具体的改进建议
        - 重构代码示例
        - 最佳实践推荐
        """
        
        task = Task(
            description=task_description,
            agent=self.agent,
            expected_output="详细的代码审查报告和重构建议"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def health_check(self) -> str:
        """检查Agent健康状态"""
        task = Task(
            description="""
            检查FastAPI后端开发环境和工具状态：
            
            **检查项目**：
            1. FastAPI依赖和版本
            2. 数据库连接状态
            3. 开发工具可用性
            4. 项目结构完整性
            5. 配置文件正确性
            
            **工具验证**：
            - SQLAlchemy模型工具
            - Alembic迁移工具
            - Pydantic Schema工具
            - API路由生成工具
            - CRUD操作工具
            
            **环境检查**：
            - Python版本兼容性
            - 虚拟环境状态
            - 依赖包完整性
            - 数据库访问权限
            """,
            agent=self.agent,
            expected_output="FastAPI开发环境健康检查报告"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()


# 创建全局FastAPI后端Agent实例
fastapi_backend_agent = FastAPIBackendAgent()


# 便捷函数
def create_resource(
    resource_name: str, 
    fields: Dict[str, str],
    include_auth: bool = True,
    custom_endpoints: List[str] = []
) -> Dict[str, str]:
    """创建完整资源的便捷函数"""
    return fastapi_backend_agent.create_complete_resource(
        resource_name, fields, include_auth, custom_endpoints
    )


def implement_endpoint(
    endpoint_path: str, 
    method: str, 
    description: str,
    include_auth: bool = True
) -> str:
    """实现API端点的便捷函数"""
    return fastapi_backend_agent.implement_api_endpoint(
        endpoint_path, method, description, include_auth
    )


def design_database(
    requirements: str,
    tables: List[str] = [],
    relationships: Dict[str, List[str]] = {}
) -> str:
    """设计数据库的便捷函数"""
    return fastapi_backend_agent.design_database_schema(
        requirements, tables, relationships
    )


def optimize_performance(target_api: str) -> str:
    """性能优化的便捷函数"""
    return fastapi_backend_agent.optimize_api_performance(target_api)


def setup_auth_system(
    auth_type: str = "JWT",
    include_rbac: bool = True,
    oauth_providers: List[str] = []
) -> str:
    """设置认证系统的便捷函数"""
    return fastapi_backend_agent.implement_authentication_system(
        auth_type, include_rbac, oauth_providers
    )


def review_code(target_files: List[str]) -> str:
    """代码审查的便捷函数"""
    return fastapi_backend_agent.code_review_and_refactor(target_files)


def check_fastapi_health() -> str:
    """健康检查的便捷函数"""
    return fastapi_backend_agent.health_check()