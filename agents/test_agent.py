"""
测试专家Agent
专门负责测试用例生成、测试执行、质量保证和测试报告
"""

from crewai import Agent, Task, Crew, Process
from typing import Dict, List, Any, Optional
from .test_tools import (
    UnitTestGenerationTool,
    APITestGenerationTool,
    MockDataGenerationTool,
    PerformanceTestGenerationTool
)
from .tools import (
    CodeAnalysisTool,
    ProjectStructureTool,
    HealthCheckTool
)


class TestAgent:
    """测试专家Agent类"""
    
    def __init__(self):
        # 测试专用工具集
        self.test_tools = [
            UnitTestGenerationTool(),
            APITestGenerationTool(),
            MockDataGenerationTool(),
            PerformanceTestGenerationTool()
        ]
        
        # 通用开发工具
        self.general_tools = [
            CodeAnalysisTool(),
            ProjectStructureTool(),
            HealthCheckTool()
        ]
        
        # 合并所有工具
        self.tools = self.test_tools + self.general_tools
        
        # 创建专家Agent
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """创建测试专家Agent"""
        return Agent(
            role='Quality Assurance & Testing Expert',
            goal='确保软件质量，提供全面的测试解决方案，包括单元测试、集成测试、API测试和性能测试',
            backstory="""
            你是一位资深的测试和质量保证专家，拥有丰富的软件测试经验和深厚的技术功底。
            你的专业技能涵盖：
            
            🧪 **测试技术专长**:
            - pytest框架深度应用和最佳实践
            - 单元测试、集成测试、端到端测试设计
            - Mock和Stub技术应用
            - 测试驱动开发(TDD)和行为驱动开发(BDD)
            - 自动化测试框架搭建和维护
            
            📊 **测试类型精通**:
            - 功能测试：单元测试、集成测试、系统测试
            - 非功能测试：性能测试、安全测试、兼容性测试
            - API测试：REST API、GraphQL、微服务测试
            - 前端测试：组件测试、E2E测试、视觉回归测试
            - 数据库测试：数据完整性、事务测试、性能测试
            
            🔧 **测试工具熟练使用**:
            - Python测试生态：pytest、unittest、nose2、tox
            - API测试：Postman、Newman、HTTPie、requests
            - 性能测试：Locust、JMeter、k6、Apache Bench
            - 前端测试：Jest、Cypress、Selenium、Playwright
            - CI/CD集成：Jenkins、GitHub Actions、GitLab CI
            
            📈 **质量管理能力**:
            - 测试策略制定和测试计划编写
            - 缺陷跟踪和回归测试管理
            - 代码覆盖率分析和质量度量
            - 测试报告生成和质量评估
            - 团队测试流程改进和培训
            
            🎯 **专业特长领域**:
            - FastAPI应用测试：路由测试、依赖注入测试、中间件测试
            - Vue.js前端测试：组件单元测试、用户交互测试
            - 数据库测试：SQLAlchemy模型测试、数据迁移测试
            - 微服务测试：服务间通信测试、契约测试
            - 安全测试：认证授权测试、输入验证测试
            
            💡 **质量保证理念**:
            - 预防缺陷优于发现缺陷
            - 测试左移和持续测试
            - 自动化优先和风险驱动测试
            - 全栈质量保证思维
            - 用户体验和业务价值导向
            
            你的目标是帮助团队建立完善的质量保证体系，确保软件产品的高质量交付。
            """,
            tools=self.tools,
            verbose=True,
            allow_delegation=False,
            max_iter=5
        )
    
    def generate_comprehensive_test_suite(
        self, 
        target_module: str,
        test_types: List[str] = None,
        coverage_level: str = "comprehensive"
    ) -> Dict[str, Any]:
        """生成全面的测试套件"""
        
        if test_types is None:
            test_types = ["unit", "integration", "api"]
        
        task_description = f"""
        为 {target_module} 生成全面的测试套件。
        
        **目标模块**: {target_module}
        **测试类型**: {test_types}
        **覆盖级别**: {coverage_level}
        
        **任务要求**:
        1. 🔍 分析目标模块的代码结构和功能
        2. 📋 制定测试策略和测试计划
        3. 🧪 生成单元测试用例
        4. 🔗 创建集成测试场景
        5. 🌐 设计API接口测试
        6. 📊 创建测试数据和Mock对象
        7. 📈 设置测试覆盖率目标
        8. 📝 生成测试执行报告
        
        **质量标准**:
        - 测试用例完整且可执行
        - 测试数据真实且有效
        - 错误场景全面覆盖
        - 断言清晰且准确
        - 测试代码规范且可维护
        
        **输出要求**:
        - 详细的测试策略文档
        - 完整的测试用例代码
        - 测试数据和夹具文件
        - 测试执行指南
        - 质量度量和覆盖率报告
        """
        
        task = Task(
            description=task_description,
            agent=self.agent,
            expected_output="完整的测试套件，包含多种测试类型和质量保证机制"
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
                'target_module': target_module,
                'test_types': test_types,
                'coverage_level': coverage_level,
                'result': result
            }
        except Exception as e:
            return {
                'status': 'error',
                'target_module': target_module,
                'error': str(e)
            }
    
    def create_api_test_suite(
        self, 
        api_endpoints: List[str],
        include_auth_tests: bool = True,
        include_performance_tests: bool = False
    ) -> str:
        """创建API测试套件"""
        
        endpoints_str = '\n'.join(f'- {endpoint}' for endpoint in api_endpoints)
        
        task_description = f"""
        为以下API端点创建完整的测试套件：
        
        **API端点列表**:
        {endpoints_str}
        
        **测试配置**:
        - 包含认证测试: {'是' if include_auth_tests else '否'}
        - 包含性能测试: {'是' if include_performance_tests else '否'}
        
        **测试任务**:
        1. 🔍 分析API端点的功能和参数
        2. ✅ 创建正常流程测试用例
        3. ❌ 设计异常情况测试场景
        4. 🔐 实现认证和权限测试
        5. 📊 生成测试数据和边界值测试
        6. 🚀 配置性能和负载测试
        7. 📋 创建测试执行脚本
        8. 📈 设置测试报告和监控
        
        **测试覆盖范围**:
        - HTTP状态码验证
        - 响应数据格式检查
        - 输入参数验证测试
        - 业务逻辑正确性验证
        - 错误处理和异常情况
        - 安全性和权限控制
        
        **输出格式**:
        - pytest测试用例文件
        - 测试配置和夹具
        - API测试数据文件
        - 性能测试脚本(如需要)
        - 测试执行和报告指南
        """
        
        task = Task(
            description=task_description,
            agent=self.agent,
            expected_output="完整的API测试套件，包含各种测试场景和自动化脚本"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def perform_test_analysis_and_optimization(
        self, 
        test_directory: str,
        analysis_type: str = "comprehensive"
    ) -> str:
        """执行测试分析和优化"""
        
        task_description = f"""
        对 {test_directory} 目录中的测试代码进行深入分析和优化。
        
        **分析目标**: {test_directory}
        **分析类型**: {analysis_type}
        
        **分析任务**:
        1. 📊 测试覆盖率分析和统计
        2. 🔍 测试用例质量评估
        3. ⚡ 测试执行性能分析
        4. 🧪 测试数据和Mock使用检查
        5. 📈 测试维护成本评估
        6. 🎯 测试策略有效性分析
        7. 💡 测试改进建议生成
        8. 🔧 测试代码重构建议
        
        **分析维度**:
        - 代码覆盖率：行覆盖率、分支覆盖率、函数覆盖率
        - 测试质量：断言质量、测试独立性、可维护性
        - 执行效率：测试运行时间、资源消耗、并行度
        - 缺陷发现能力：边界值测试、异常处理、回归测试
        - 可读性和可维护性：命名规范、结构清晰度、注释质量
        
        **优化建议包括**:
        - 提高覆盖率的具体方案
        - 改进测试用例设计
        - 优化测试执行性能
        - 重构重复和冗余代码
        - 增强测试数据管理
        - 完善CI/CD集成
        
        **输出要求**:
        - 详细的分析报告
        - 具体的优化建议
        - 重构代码示例
        - 改进实施计划
        """
        
        task = Task(
            description=task_description,
            agent=self.agent,
            expected_output="详细的测试分析报告和优化改进方案"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def create_performance_test_plan(
        self, 
        target_application: str,
        test_scenarios: List[str] = None,
        performance_targets: Dict[str, Any] = None
    ) -> str:
        """创建性能测试计划"""
        
        if test_scenarios is None:
            test_scenarios = ["负载测试", "压力测试", "峰值测试"]
        
        if performance_targets is None:
            performance_targets = {
                "响应时间": "< 200ms",
                "吞吐量": "> 1000 QPS", 
                "并发用户": "100-500",
                "CPU使用率": "< 70%",
                "内存使用": "< 80%"
            }
        
        scenarios_str = '\n'.join(f'- {scenario}' for scenario in test_scenarios)
        targets_str = '\n'.join(f'- {key}: {value}' for key, value in performance_targets.items())
        
        task_description = f"""
        为 {target_application} 应用创建全面的性能测试计划。
        
        **目标应用**: {target_application}
        
        **测试场景**:
        {scenarios_str}
        
        **性能目标**:
        {targets_str}
        
        **测试计划任务**:
        1. 📋 性能测试策略制定
        2. 🎯 关键性能指标(KPI)定义
        3. 🧪 测试场景设计和用例编写
        4. 📊 测试数据准备和环境配置
        5. 🔧 测试工具选择和脚本开发
        6. 📈 监控指标设置和基线建立
        7. ⚠️ 风险评估和应急预案
        8. 📅 测试执行计划和时间安排
        
        **测试类型设计**:
        - 负载测试：模拟正常业务负载
        - 压力测试：测试系统极限容量
        - 峰值测试：模拟突发流量冲击
        - 稳定性测试：长时间运行稳定性
        - 容量规划：系统扩展性评估
        
        **工具和技术**:
        - 负载生成：Locust、JMeter、k6
        - 监控工具：Prometheus、Grafana、APM
        - 数据分析：性能报告、趋势分析
        - CI/CD集成：自动化性能回归测试
        
        **交付成果**:
        - 性能测试计划文档
        - 测试脚本和配置文件
        - 监控仪表板配置
        - 测试执行手册
        - 性能基线和报告模板
        """
        
        task = Task(
            description=task_description,
            agent=self.agent,
            expected_output="完整的性能测试计划和实施方案"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def generate_test_data_strategy(
        self, 
        data_models: List[str],
        test_environments: List[str] = None,
        data_privacy_requirements: bool = True
    ) -> str:
        """生成测试数据策略"""
        
        if test_environments is None:
            test_environments = ["development", "testing", "staging"]
        
        models_str = '\n'.join(f'- {model}' for model in data_models)
        envs_str = '\n'.join(f'- {env}' for env in test_environments)
        
        task_description = f"""
        为数据模型创建全面的测试数据策略和管理方案。
        
        **数据模型**:
        {models_str}
        
        **目标环境**:
        {envs_str}
        
        **隐私保护要求**: {'是' if data_privacy_requirements else '否'}
        
        **策略制定任务**:
        1. 📊 测试数据需求分析
        2. 🏗️ 数据模型关系梳理
        3. 🎲 测试数据生成策略
        4. 🔐 数据脱敏和隐私保护
        5. 📚 测试数据管理流程
        6. 🔄 数据维护和更新机制
        7. 🚀 数据部署和分发策略
        8. 📈 数据质量监控和验证
        
        **数据生成方法**:
        - Factory模式：使用factory_boy生成结构化数据
        - Faker库：生成逼真的假数据
        - 数据采样：从生产环境安全采样
        - 手工构造：针对特殊场景的精确数据
        - 数据变异：基于现有数据生成变体
        
        **数据分类管理**:
        - 基础数据：用户、角色、权限等核心数据
        - 业务数据：订单、产品、交易等业务实体
        - 关联数据：实体间关系和外键数据
        - 边界数据：极值、异常、空值等边界情况
        - 性能数据：大量数据用于性能测试
        
        **隐私保护措施**:
        - 数据脱敏：敏感信息替换和掩码
        - 数据分级：按敏感度分类管理
        - 访问控制：数据访问权限管理
        - 审计日志：数据使用记录和追踪
        - 合规检查：GDPR、CCPA等法规遵循
        
        **交付成果**:
        - 测试数据策略文档
        - 数据生成脚本和工具
        - 数据管理流程规范
        - 隐私保护实施指南
        - 数据质量验证工具
        """
        
        task = Task(
            description=task_description,
            agent=self.agent,
            expected_output="全面的测试数据策略和管理实施方案"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def create_frontend_test_suite(
        self, 
        frontend_components: List[str],
        test_types: List[str] = None
    ) -> str:
        """创建前端测试套件"""
        
        if test_types is None:
            test_types = ["unit", "component", "e2e"]
        
        components_str = '\n'.join(f'- {component}' for component in frontend_components)
        types_str = '\n'.join(f'- {test_type}' for test_type in test_types)
        
        task_description = f"""
        为Vue.js前端组件创建全面的测试套件。
        
        **目标组件**:
        {components_str}
        
        **测试类型**:
        {types_str}
        
        **测试任务**:
        1. 🧪 组件单元测试：Props、事件、方法测试
        2. 🎨 UI组件测试：渲染、样式、交互测试
        3. 🔗 集成测试：组件间通信和数据流测试
        4. 🌐 端到端测试：完整用户流程测试
        5. 📱 响应式测试：不同屏幕尺寸适配测试
        6. ♿ 可访问性测试：ARIA、键盘导航等
        7. 🚀 性能测试：渲染性能和内存使用
        8. 🔄 状态管理测试：Vuex/Pinia状态测试
        
        **前端测试技术栈**:
        - 单元测试：Jest + Vue Test Utils
        - 组件测试：@vue/test-utils + Testing Library
        - E2E测试：Cypress或Playwright
        - 视觉回归：Percy、Chromatic
        - 性能测试：Lighthouse CI
        
        **测试场景设计**:
        - 正常渲染：组件正常显示和功能
        - 数据绑定：Props和数据响应性
        - 用户交互：点击、输入、表单提交
        - 错误处理：异常状态和错误边界
        - 路由导航：页面跳转和参数传递
        - 状态管理：全局状态变更和同步
        
        **质量标准**:
        - 测试覆盖率 > 80%
        - 组件API完整测试
        - 用户交互路径覆盖
        - 异常情况处理验证
        - 性能指标达标
        
        **输出要求**:
        - Jest测试配置和脚本
        - 组件测试用例文件
        - E2E测试场景脚本
        - 测试数据和Mock文件
        - 测试执行和CI集成指南
        """
        
        task = Task(
            description=task_description,
            agent=self.agent,
            expected_output="完整的前端测试套件和执行框架"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def health_check(self) -> str:
        """检查测试Agent健康状态"""
        task = Task(
            description="""
            检查测试环境和工具链的健康状态：
            
            **检查项目**:
            1. pytest框架和插件状态
            2. 测试数据库连接和配置
            3. Mock工具和测试夹具
            4. 代码覆盖率工具配置
            5. CI/CD测试流水线状态
            6. 性能测试工具可用性
            7. 前端测试环境配置
            
            **工具验证**:
            - pytest和相关插件
            - httpx/requests用于API测试
            - factory_boy用于数据生成
            - Locust用于性能测试
            - Jest/Cypress用于前端测试
            
            **环境检查**:
            - 测试数据库连接
            - Redis缓存测试环境
            - 测试文件目录结构
            - 配置文件正确性
            - 依赖包完整性
            
            **质量度量**:
            - 当前测试覆盖率统计
            - 测试执行时间分析
            - 失败测试用例统计
            - 测试代码质量评估
            """,
            agent=self.agent,
            expected_output="测试环境和工具链健康检查报告"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()


# 创建全局测试Agent实例
test_agent = TestAgent()


# 便捷函数
def generate_unit_tests(
    source_file: str,
    test_type: str = "unit",
    coverage_level: str = "comprehensive"
) -> Dict[str, Any]:
    """生成单元测试的便捷函数"""
    return test_agent.generate_comprehensive_test_suite(
        source_file, [test_type], coverage_level
    )


def create_api_tests(
    api_endpoints: List[str],
    include_auth: bool = True,
    include_performance: bool = False
) -> str:
    """创建API测试的便捷函数"""
    return test_agent.create_api_test_suite(
        api_endpoints, include_auth, include_performance
    )


def analyze_test_quality(test_directory: str) -> str:
    """分析测试质量的便捷函数"""
    return test_agent.perform_test_analysis_and_optimization(test_directory)


def create_performance_tests(
    target_app: str,
    scenarios: List[str] = None,
    targets: Dict[str, Any] = None
) -> str:
    """创建性能测试的便捷函数"""
    return test_agent.create_performance_test_plan(target_app, scenarios, targets)


def create_test_data_plan(
    data_models: List[str],
    environments: List[str] = None
) -> str:
    """创建测试数据计划的便捷函数"""
    return test_agent.generate_test_data_strategy(data_models, environments)


def create_frontend_tests(
    components: List[str],
    test_types: List[str] = None
) -> str:
    """创建前端测试的便捷函数"""
    return test_agent.create_frontend_test_suite(components, test_types)


def check_test_health() -> str:
    """测试环境健康检查的便捷函数"""
    return test_agent.health_check()