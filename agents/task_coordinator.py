"""
任务分配协调Agent
负责智能任务分解、分配和工作流管理
"""

from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import json
from crewai import Agent, Task, Crew, Process

from .tools import (
    DocumentationGenerationTool,
    CodeAnalysisTool,
    ProjectStructureTool,
    ImprovementSuggestionTool,
    HealthCheckTool
)


class TaskType(Enum):
    """任务类型枚举"""
    DOCUMENTATION = "documentation"
    CODE_ANALYSIS = "code_analysis"
    API_DEVELOPMENT = "api_development"
    TESTING = "testing"
    REFACTORING = "refactoring"
    DEPLOYMENT = "deployment"
    SECURITY_AUDIT = "security_audit"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"


class TaskPriority(Enum):
    """任务优先级枚举"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class TaskInfo:
    """任务信息数据结构"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    task_type: TaskType = TaskType.DOCUMENTATION
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    estimated_duration: int = 30  # 分钟
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentInfo:
    """Agent信息数据结构"""
    name: str
    capabilities: List[TaskType]
    max_concurrent_tasks: int = 3
    current_tasks: List[str] = field(default_factory=list)
    is_available: bool = True
    performance_score: float = 1.0  # 性能评分


class TaskCoordinatorAgent:
    """任务协调Agent类"""
    
    def __init__(self):
        # 任务和Agent管理
        self.tasks: Dict[str, TaskInfo] = {}
        self.agents: Dict[str, AgentInfo] = {}
        self.task_queue: List[str] = []
        self.completed_tasks: List[str] = []
        
        # 初始化工具集
        self.tools = [
            DocumentationGenerationTool(),
            CodeAnalysisTool(),
            ProjectStructureTool(),
            ImprovementSuggestionTool(),
            HealthCheckTool()
        ]
        
        # 创建协调Agent
        self.agent = self._create_agent()
        
        # 注册默认Agent
        self._register_default_agents()
    
    def _create_agent(self) -> Agent:
        """创建任务协调专家Agent"""
        return Agent(
            role='Task Coordinator & Project Manager',
            goal='智能分析项目需求，分解复杂任务，协调多个专业Agent高效完成工作',
            backstory="""
            你是一位资深的项目管理专家和技术架构师，拥有丰富的软件开发项目管理经验。
            你的核心技能包括：
            
            🎯 **核心能力**:
            - 需求分析和任务分解
            - 资源调度和优先级管理
            - 多Agent协调和工作流设计
            - 项目进度跟踪和质量控制
            - 风险识别和问题解决
            
            💼 **管理风格**:
            - 数据驱动的决策制定
            - 敏捷开发理念
            - 持续改进和优化
            - 团队协作和沟通
            
            🔧 **技术专长**:
            - FastAPI和Python后端开发
            - Vue.js前端开发
            - 数据库设计和优化
            - DevOps和CI/CD流程
            - 代码质量和安全审查
            
            你的目标是确保项目高效执行，质量可控，按时交付。
            """,
            tools=self.tools,
            verbose=True,
            allow_delegation=True,
            max_iter=5
        )
    
    def _register_default_agents(self):
        """注册默认可用的Agent"""
        # 文档生成Agent
        self.register_agent(
            name="documentation_agent",
            capabilities=[
                TaskType.DOCUMENTATION,
                TaskType.CODE_ANALYSIS
            ],
            max_concurrent_tasks=2
        )
        
        # FastAPI后端开发Agent
        self.register_agent(
            name="fastapi_backend_agent",
            capabilities=[
                TaskType.API_DEVELOPMENT,
                TaskType.CODE_ANALYSIS,
                TaskType.REFACTORING,
                TaskType.PERFORMANCE_OPTIMIZATION
            ],
            max_concurrent_tasks=3
        )
        
        # 测试专家Agent
        self.register_agent(
            name="test_agent",
            capabilities=[
                TaskType.TESTING,
                TaskType.CODE_ANALYSIS,
                TaskType.PERFORMANCE_OPTIMIZATION
            ],
            max_concurrent_tasks=4
        )
        
        # 部署专家Agent
        self.register_agent(
            name="deployment_agent",
            capabilities=[
                TaskType.DEPLOYMENT,
                TaskType.PERFORMANCE_OPTIMIZATION,
                TaskType.SECURITY_AUDIT
            ],
            max_concurrent_tasks=3
        )
    
    def register_agent(
        self, 
        name: str, 
        capabilities: List[TaskType], 
        max_concurrent_tasks: int = 3
    ) -> bool:
        """注册新Agent"""
        try:
            self.agents[name] = AgentInfo(
                name=name,
                capabilities=capabilities,
                max_concurrent_tasks=max_concurrent_tasks
            )
            return True
        except Exception as e:
            print(f"❌ Agent注册失败: {e}")
            return False
    
    def create_task(
        self,
        title: str,
        description: str,
        task_type: TaskType,
        priority: TaskPriority = TaskPriority.MEDIUM,
        dependencies: List[str] = None,
        estimated_duration: int = 30,
        metadata: Dict[str, Any] = None
    ) -> str:
        """创建新任务"""
        task = TaskInfo(
            title=title,
            description=description,
            task_type=task_type,
            priority=priority,
            dependencies=dependencies or [],
            estimated_duration=estimated_duration,
            metadata=metadata or {}
        )
        
        self.tasks[task.id] = task
        self.task_queue.append(task.id)
        
        # 按优先级排序任务队列
        self.task_queue.sort(key=lambda tid: self.tasks[tid].priority.value, reverse=True)
        
        return task.id
    
    def decompose_user_request(self, user_request: str) -> List[str]:
        """分解用户请求为子任务"""
        decomposition_prompt = f"""
        分析用户请求并分解为具体的可执行子任务：
        
        用户请求: {user_request}
        
        请按以下格式输出任务分解结果：
        1. 识别主要功能需求
        2. 分解为具体的技术任务
        3. 确定任务优先级和依赖关系
        4. 估算每个任务的工作量
        
        输出格式：JSON格式的任务列表
        """
        
        task = Task(
            description=decomposition_prompt,
            agent=self.agent,
            expected_output="JSON格式的任务分解结果，包含任务标题、描述、类型、优先级等信息"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        try:
            result = crew.kickoff()
            # 解析结果并创建任务
            task_ids = self._parse_and_create_tasks(result)
            return task_ids
        except Exception as e:
            print(f"❌ 任务分解失败: {e}")
            return []
    
    def _parse_and_create_tasks(self, decomposition_result: str) -> List[str]:
        """解析分解结果并创建任务"""
        task_ids = []
        
        try:
            # 尝试解析JSON（简化处理，实际需要更robust的解析）
            lines = decomposition_result.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('#'):
                    # 智能任务类型识别
                    if '文档' in line or 'API文档' in line or 'documentation' in line:
                        task_type = TaskType.DOCUMENTATION
                    elif '测试' in line or 'test' in line or 'testing' in line:
                        task_type = TaskType.TESTING
                    elif '开发' in line or '实现' in line or 'API开发' in line or 'development' in line:
                        task_type = TaskType.API_DEVELOPMENT
                    elif '优化' in line or '性能' in line or 'optimize' in line or 'performance' in line:
                        task_type = TaskType.PERFORMANCE_OPTIMIZATION
                    elif '重构' in line or 'refactor' in line or '改进' in line:
                        task_type = TaskType.REFACTORING
                    else:
                        task_type = TaskType.CODE_ANALYSIS
                    
                    task_id = self.create_task(
                        title=line.strip()[:50],
                        description=line.strip(),
                        task_type=task_type,
                        priority=TaskPriority.MEDIUM
                    )
                    task_ids.append(task_id)
        except Exception as e:
            print(f"⚠️ 任务解析失败，使用默认分解: {e}")
            # 创建默认任务
            task_id = self.create_task(
                title="用户需求处理",
                description=decomposition_result,
                task_type=TaskType.DOCUMENTATION
            )
            task_ids.append(task_id)
        
        return task_ids
    
    def find_best_agent(self, task_id: str) -> Optional[str]:
        """为任务寻找最合适的Agent"""
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        # 筛选具备相关能力的Agent
        capable_agents = []
        for agent_name, agent_info in self.agents.items():
            if (task.task_type in agent_info.capabilities and 
                agent_info.is_available and 
                len(agent_info.current_tasks) < agent_info.max_concurrent_tasks):
                capable_agents.append((agent_name, agent_info))
        
        if not capable_agents:
            return None
        
        # 选择性能最好且负载最轻的Agent
        best_agent = min(
            capable_agents,
            key=lambda x: (len(x[1].current_tasks), -x[1].performance_score)
        )
        
        return best_agent[0]
    
    def assign_task(self, task_id: str, agent_name: str = None) -> bool:
        """分配任务给Agent"""
        task = self.tasks.get(task_id)
        if not task or task.status != TaskStatus.PENDING:
            return False
        
        # 检查依赖任务是否完成
        for dep_id in task.dependencies:
            dep_task = self.tasks.get(dep_id)
            if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                task.status = TaskStatus.BLOCKED
                return False
        
        # 自动选择Agent
        if not agent_name:
            agent_name = self.find_best_agent(task_id)
        
        if not agent_name or agent_name not in self.agents:
            return False
        
        # 执行分配
        agent_info = self.agents[agent_name]
        if len(agent_info.current_tasks) >= agent_info.max_concurrent_tasks:
            return False
        
        task.assigned_agent = agent_name
        task.status = TaskStatus.ASSIGNED
        agent_info.current_tasks.append(task_id)
        
        return True
    
    def execute_task(self, task_id: str) -> bool:
        """执行任务"""
        task = self.tasks.get(task_id)
        if not task or task.status != TaskStatus.ASSIGNED:
            return False
        
        try:
            task.status = TaskStatus.IN_PROGRESS
            task.started_at = datetime.now()
            
            # 根据任务类型执行相应的操作
            if task.task_type == TaskType.DOCUMENTATION:
                result = self._execute_documentation_task(task)
            elif task.task_type == TaskType.CODE_ANALYSIS:
                result = self._execute_analysis_task(task)
            elif task.task_type == TaskType.API_DEVELOPMENT:
                result = self._execute_api_development_task(task)
            elif task.task_type == TaskType.REFACTORING:
                result = self._execute_refactoring_task(task)
            elif task.task_type == TaskType.PERFORMANCE_OPTIMIZATION:
                result = self._execute_performance_task(task)
            elif task.task_type == TaskType.TESTING:
                result = self._execute_testing_task(task)
            elif task.task_type == TaskType.DEPLOYMENT:
                result = self._execute_deployment_task(task)
            else:
                result = f"任务类型 {task.task_type.value} 的执行逻辑待实现"
            
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            
            # 清理Agent分配
            if task.assigned_agent:
                agent_info = self.agents[task.assigned_agent]
                if task_id in agent_info.current_tasks:
                    agent_info.current_tasks.remove(task_id)
            
            self.completed_tasks.append(task_id)
            if task_id in self.task_queue:
                self.task_queue.remove(task_id)
            
            return True
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            print(f"❌ 任务执行失败: {e}")
            return False
    
    def _execute_documentation_task(self, task: TaskInfo) -> str:
        """执行文档生成任务"""
        from .doc_agent import doc_agent
        
        # 根据任务描述选择合适的文档生成方法
        if 'API' in task.description or 'api' in task.description:
            target = task.metadata.get('target', 'backend/api')
            return doc_agent.generate_api_documentation(target)
        elif 'README' in task.description:
            return doc_agent.generate_readme()
        else:
            target = task.metadata.get('target', task.title)
            return doc_agent.analyze_and_document(target)
    
    def _execute_analysis_task(self, task: TaskInfo) -> str:
        """执行代码分析任务"""
        from .claude_integration import claude_integration
        
        target = task.metadata.get('target', task.title)
        return claude_integration.analyze_file(target)
    
    def _execute_api_development_task(self, task: TaskInfo) -> str:
        """执行API开发任务"""
        try:
            from .fastapi_agent import fastapi_backend_agent
            
            # 根据任务描述选择合适的API开发方法
            if 'resource' in task.description.lower() or 'crud' in task.description.lower():
                # 创建完整资源
                resource_name = task.metadata.get('resource_name', 'example')
                fields = task.metadata.get('fields', {'name': 'string', 'description': 'text'})
                result = fastapi_backend_agent.create_complete_resource(resource_name, fields)
                return result.get('result', str(result))
            elif 'endpoint' in task.description.lower():
                # 实现单个端点
                endpoint_path = task.metadata.get('endpoint_path', '/example')
                method = task.metadata.get('method', 'GET')
                return fastapi_backend_agent.implement_api_endpoint(endpoint_path, method, task.description)
            else:
                # 通用API开发任务
                return f"正在开发API功能: {task.description}"
        except ImportError:
            return "FastAPI Agent 未正确安装或配置"
    
    def _execute_refactoring_task(self, task: TaskInfo) -> str:
        """执行代码重构任务"""
        try:
            from .fastapi_agent import fastapi_backend_agent
            
            target_files = task.metadata.get('target_files', [])
            if not target_files:
                target_files = [task.metadata.get('target', 'backend/')]
            
            return fastapi_backend_agent.code_review_and_refactor(target_files)
        except ImportError:
            return "FastAPI Agent 未正确安装或配置"
    
    def _execute_performance_task(self, task: TaskInfo) -> str:
        """执行性能优化任务"""
        try:
            from .fastapi_agent import fastapi_backend_agent
            
            target_api = task.metadata.get('target_api', task.title)
            return fastapi_backend_agent.optimize_api_performance(target_api)
        except ImportError:
            return "FastAPI Agent 未正确安装或配置"
    
    def _execute_testing_task(self, task: TaskInfo) -> str:
        """执行测试任务"""
        try:
            from .test_agent import test_agent
            
            # 根据任务描述选择合适的测试方法
            if 'unit' in task.description.lower() or '单元测试' in task.description:
                # 单元测试
                source_file = task.metadata.get('source_file', '')
                if source_file:
                    result = test_agent.generate_comprehensive_test_suite(source_file, ["unit"])
                    return result.get('result', str(result))
                else:
                    return "缺少源文件参数，无法生成单元测试"
            
            elif 'api' in task.description.lower() or 'API测试' in task.description:
                # API测试
                endpoints = task.metadata.get('endpoints', [])
                if endpoints:
                    return test_agent.create_api_test_suite(endpoints)
                else:
                    return "缺少API端点信息，无法生成API测试"
            
            elif 'performance' in task.description.lower() or '性能测试' in task.description:
                # 性能测试
                target_app = task.metadata.get('target_app', task.title)
                return test_agent.create_performance_test_plan(target_app)
            
            elif 'frontend' in task.description.lower() or '前端测试' in task.description:
                # 前端测试
                components = task.metadata.get('components', [])
                if components:
                    return test_agent.create_frontend_test_suite(components)
                else:
                    return "缺少组件信息，无法生成前端测试"
            
            else:
                # 通用测试任务
                target = task.metadata.get('target', task.title)
                result = test_agent.generate_comprehensive_test_suite(target)
                return result.get('result', str(result))
                
        except ImportError:
            return "Test Agent 未正确安装或配置"
    
    def _execute_deployment_task(self, task: TaskInfo) -> str:
        """执行部署任务"""
        try:
            from .deployment_agent import deployment_agent
            
            # 根据任务描述选择合适的部署方法
            if 'containerize' in task.description.lower() or '容器化' in task.description:
                # 容器化任务
                services = task.metadata.get('services', ['backend', 'frontend'])
                environment = task.metadata.get('environment', 'production')
                result = deployment_agent.containerize_application(services, environment)
                return f"✅ 容器化完成: {result.get('status', 'success')}"
            
            elif 'cicd' in task.description.lower() or 'pipeline' in task.description.lower() or '流水线' in task.description:
                # CI/CD流水线设置
                platform = task.metadata.get('platform', 'github')
                features = task.metadata.get('features', ['automated_testing', 'docker_build'])
                result = deployment_agent.setup_cicd_pipeline(platform, features)
                return f"✅ CI/CD流水线设置完成: {result.get('status', 'success')}"
            
            elif 'environment' in task.description.lower() or '环境配置' in task.description:
                # 环境配置
                environments = task.metadata.get('environments', ['development', 'production'])
                result = deployment_agent.configure_environments(environments)
                return f"✅ 环境配置完成: {result.get('status', 'success')}"
            
            elif 'monitoring' in task.description.lower() or '监控' in task.description:
                # 监控设置
                services = task.metadata.get('services', ['backend', 'frontend'])
                monitoring_stack = task.metadata.get('monitoring_stack', 'prometheus')
                result = deployment_agent.setup_monitoring_stack(services, monitoring_stack)
                return f"✅ 监控系统设置完成: {result.get('status', 'success')}"
            
            elif 'optimize' in task.description.lower() or '优化' in task.description:
                # 性能优化
                environment = task.metadata.get('environment', 'production')
                areas = task.metadata.get('optimization_areas', ['container_optimization'])
                result = deployment_agent.optimize_deployment_performance(environment, areas)
                return f"✅ 部署性能优化完成: {result.get('status', 'success')}"
            
            elif 'disaster' in task.description.lower() or 'recovery' in task.description.lower() or '灾难恢复' in task.description:
                # 灾难恢复计划
                services = task.metadata.get('services', ['backend', 'db'])
                objectives = task.metadata.get('recovery_objectives', {'RTO': '30分钟', 'RPO': '5分钟'})
                result = deployment_agent.create_disaster_recovery_plan(services, objectives)
                return f"✅ 灾难恢复计划创建完成: {result.get('status', 'success')}"
            
            else:
                # 通用部署任务
                services = task.metadata.get('services', ['backend', 'frontend'])
                result = deployment_agent.containerize_application(services)
                return f"✅ 通用部署任务完成: {result.get('status', 'success')}"
                
        except ImportError:
            return "Deployment Agent 未正确安装或配置"
        except Exception as e:
            return f"❌ 部署任务执行失败: {str(e)}"
    
    def process_queue(self, max_concurrent: int = 3) -> Dict[str, Any]:
        """处理任务队列"""
        results = {
            'processed': 0,
            'completed': 0,
            'failed': 0,
            'details': []
        }
        
        # 处理等待中的任务
        processed_count = 0
        for task_id in self.task_queue[:]:
            if processed_count >= max_concurrent:
                break
                
            task = self.tasks[task_id]
            if task.status == TaskStatus.PENDING:
                if self.assign_task(task_id):
                    if self.execute_task(task_id):
                        results['completed'] += 1
                    else:
                        results['failed'] += 1
                    processed_count += 1
                    results['processed'] += 1
                    
                    results['details'].append({
                        'task_id': task_id,
                        'title': task.title,
                        'status': task.status.value,
                        'result': task.result[:100] if task.result else None
                    })
        
        return results
    
    def get_status_report(self) -> Dict[str, Any]:
        """获取状态报告"""
        total_tasks = len(self.tasks)
        status_counts = {}
        
        for task in self.tasks.values():
            status_counts[task.status.value] = status_counts.get(task.status.value, 0) + 1
        
        agent_status = {}
        for name, agent in self.agents.items():
            agent_status[name] = {
                'available': agent.is_available,
                'current_tasks': len(agent.current_tasks),
                'max_tasks': agent.max_concurrent_tasks,
                'utilization': len(agent.current_tasks) / agent.max_concurrent_tasks
            }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_tasks': total_tasks,
            'task_status': status_counts,
            'queue_length': len(self.task_queue),
            'completed_tasks': len(self.completed_tasks),
            'agent_status': agent_status,
            'system_health': self._check_system_health()
        }
    
    def _check_system_health(self) -> Dict[str, Any]:
        """检查系统健康状态"""
        try:
            health_tool = HealthCheckTool()
            health_result = health_tool._run()
            
            return {
                'status': 'healthy' if '✅' in health_result else 'warning',
                'details': health_result
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def handle_user_request(self, request: str, auto_execute: bool = True) -> Dict[str, Any]:
        """处理用户请求的主入口"""
        try:
            # 1. 分解用户请求
            task_ids = self.decompose_user_request(request)
            
            result = {
                'request': request,
                'created_tasks': len(task_ids),
                'task_ids': task_ids,
                'execution_results': []
            }
            
            # 2. 自动执行任务（如果启用）
            if auto_execute and task_ids:
                execution_results = self.process_queue(max_concurrent=len(task_ids))
                result['execution_results'] = execution_results
            
            return result
            
        except Exception as e:
            return {
                'request': request,
                'error': str(e),
                'created_tasks': 0,
                'task_ids': []
            }


# 创建全局任务协调器实例
task_coordinator = TaskCoordinatorAgent()


# 便捷函数
def handle_request(request: str, auto_execute: bool = True) -> Dict[str, Any]:
    """处理用户请求的便捷函数"""
    return task_coordinator.handle_user_request(request, auto_execute)


def get_system_status() -> Dict[str, Any]:
    """获取系统状态的便捷函数"""
    return task_coordinator.get_status_report()


def register_new_agent(name: str, capabilities: List[TaskType], max_tasks: int = 3) -> bool:
    """注册新Agent的便捷函数"""
    return task_coordinator.register_agent(name, capabilities, max_tasks)


def create_manual_task(
    title: str, 
    description: str, 
    task_type: TaskType, 
    priority: TaskPriority = TaskPriority.MEDIUM
) -> str:
    """手动创建任务的便捷函数"""
    return task_coordinator.create_task(title, description, task_type, priority)


def execute_task_by_id(task_id: str) -> bool:
    """执行指定任务的便捷函数"""
    if task_coordinator.assign_task(task_id):
        return task_coordinator.execute_task(task_id)
    return False