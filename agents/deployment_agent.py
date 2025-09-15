"""
部署专家Agent
专门负责DevOps部署、CI/CD流水线、环境管理、容器化和监控配置
"""

from crewai import Agent, Task, Crew, Process
from typing import Dict, List, Optional, Any, Union
from .tools import (
    DocumentationGenerationTool,
    CodeAnalysisTool,
    ProjectStructureTool,
    HealthCheckTool
)
from .deployment_tools import (
    DockerManagementTool,
    CICDPipelineTool,
    EnvironmentManagementTool,
    MonitoringSetupTool
)


class DeploymentAgent:
    """部署专家Agent类"""
    
    def __init__(self):
        self.tools = [
            DockerManagementTool(),
            CICDPipelineTool(),
            EnvironmentManagementTool(),
            MonitoringSetupTool(),
            DocumentationGenerationTool(),
            CodeAnalysisTool(),
            ProjectStructureTool(),
            HealthCheckTool()
        ]
        
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """创建部署专家Agent"""
        return Agent(
            role='DevOps & Deployment Specialist',
            goal='设计和实施高可用、可扩展的部署架构，确保应用的稳定运行和持续交付',
            backstory="""
            你是一位经验丰富的DevOps和部署专家，在云原生技术和持续集成/持续部署方面有深厚的专业知识。
            你的专长包括：
            
            🐳 **容器化和编排技术**:
            - Docker容器化最佳实践和优化
            - Kubernetes集群管理和服务编排
            - Docker Compose多服务编排
            - 容器镜像构建和安全扫描
            - 微服务架构部署策略
            
            🚀 **CI/CD流水线设计**:
            - GitHub Actions工作流设计
            - GitLab CI/CD流水线配置
            - Jenkins自动化构建部署
            - 多环境部署策略(蓝绿、金丝雀、滚动)
            - 自动化测试集成和质量门禁
            
            🏗️ **基础设施即代码**:
            - Terraform基础设施管理
            - Ansible配置管理
            - 云平台服务配置(AWS、Azure、GCP)
            - 网络安全和负载均衡配置
            - 存储和数据库高可用配置
            
            📊 **监控和可观测性**:
            - Prometheus + Grafana监控栈
            - ELK日志聚合和分析
            - APM性能监控集成
            - 告警规则和事件响应
            - 服务健康检查和自动恢复
            
            🔒 **安全和合规**:
            - 容器和镜像安全扫描
            - 密钥管理和访问控制
            - 网络隔离和防火墙配置
            - 安全审计和合规检查
            - 漏洞管理和修复流程
            
            ⚡ **性能优化**:
            - 应用性能调优
            - 资源利用率优化
            - 自动扩缩容配置
            - CDN和缓存策略
            - 数据库性能优化
            
            你始终关注自动化、可靠性、安全性和可维护性，能够为不同规模的项目提供最适合的部署解决方案。
            """,
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            max_iter=3,
            memory=True
        )
    
    def containerize_application(self, services: List[str], environment: str = "production",
                               optimization_level: str = "standard") -> Dict[str, Any]:
        """容器化应用服务"""
        try:
            results = {
                'containerization_plan': [],
                'docker_files': {},
                'compose_config': '',
                'optimization_recommendations': [],
                'status': 'success'
            }
            
            # 分析每个服务的容器化需求
            docker_tool = DockerManagementTool()
            
            for service in services:
                # 生成Dockerfile
                dockerfile_result = docker_tool._run(
                    action="generate_dockerfile",
                    service_type=service,
                    optimization_level=optimization_level
                )
                results['docker_files'][service] = dockerfile_result
                results['containerization_plan'].append(f"✅ {service} 服务容器化完成")
            
            # 生成Docker Compose配置
            compose_result = docker_tool._run(
                action="generate_compose",
                environment=environment,
                services=services
            )
            results['compose_config'] = compose_result
            
            # 生成优化建议
            optimization_result = docker_tool._run(
                action="optimize_images",
                services=services
            )
            results['optimization_recommendations'] = optimization_result
            
            return results
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def setup_cicd_pipeline(self, platform: str = "github", 
                           pipeline_features: List[str] = None,
                           environments: List[str] = None) -> Dict[str, Any]:
        """设置CI/CD流水线"""
        try:
            pipeline_features = pipeline_features or [
                "automated_testing", "code_quality", "docker_build", "multi_env_deploy"
            ]
            environments = environments or ["development", "staging", "production"]
            
            cicd_tool = CICDPipelineTool()
            
            results = {
                'workflow_config': '',
                'pipeline_setup': '',
                'deployment_strategy': '',
                'quality_gates': '',
                'status': 'success'
            }
            
            # 生成工作流配置
            workflow_result = cicd_tool._run(
                action="generate_workflow",
                workflow_type="full_cicd",
                environments=environments
            )
            results['workflow_config'] = workflow_result
            
            # 设置流水线
            pipeline_result = cicd_tool._run(
                action="setup_pipeline",
                platform=platform,
                features=pipeline_features
            )
            results['pipeline_setup'] = pipeline_result
            
            # 创建部署策略
            strategy_result = cicd_tool._run(
                action="deploy_strategy",
                strategy_type="blue_green",
                environments=environments
            )
            results['deployment_strategy'] = strategy_result
            
            # 设置质量门禁
            gates_result = cicd_tool._run(
                action="quality_gates",
                checks=["test_coverage", "code_quality", "security_scan"]
            )
            results['quality_gates'] = gates_result
            
            return results
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def configure_environments(self, environments: List[str], 
                             config_type: str = "docker") -> Dict[str, Any]:
        """配置多环境部署"""
        try:
            env_tool = EnvironmentManagementTool()
            
            results = {
                'environment_configs': {},
                'secret_management': {},
                'validation_results': {},
                'status': 'success'
            }
            
            for env in environments:
                # 创建环境配置
                config_result = env_tool._run(
                    action="create_env_config",
                    environment=env,
                    services=["backend", "frontend", "db", "redis"],
                    config_type=config_type
                )
                results['environment_configs'][env] = config_result
                
                # 生成密钥管理配置
                secret_result = env_tool._run(
                    action="manage_secrets",
                    action="generate",
                    environment=env
                )
                results['secret_management'][env] = secret_result
                
                # 验证配置
                validation_result = env_tool._run(
                    action="validate_config",
                    environment=env
                )
                results['validation_results'][env] = validation_result
            
            return results
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def setup_monitoring_stack(self, services: List[str], 
                             monitoring_stack: str = "prometheus",
                             alert_types: List[str] = None) -> Dict[str, Any]:
        """设置监控和告警系统"""
        try:
            alert_types = alert_types or [
                "high_error_rate", "high_response_time", 
                "database_connection_high", "memory_usage_high"
            ]
            
            monitoring_tool = MonitoringSetupTool()
            
            results = {
                'monitoring_config': '',
                'logging_config': '',
                'alert_rules': '',
                'dashboard_config': '',
                'status': 'success'
            }
            
            # 设置应用监控
            monitoring_result = monitoring_tool._run(
                action="setup_monitoring",
                services=services,
                monitoring_stack=monitoring_stack
            )
            results['monitoring_config'] = monitoring_result
            
            # 配置日志系统
            logging_result = monitoring_tool._run(
                action="configure_logging",
                log_level="INFO",
                output_format="json"
            )
            results['logging_config'] = logging_result
            
            # 创建告警规则
            alert_result = monitoring_tool._run(
                action="create_alerts",
                alert_types=alert_types
            )
            results['alert_rules'] = alert_result
            
            # 设置监控仪表板
            dashboard_result = monitoring_tool._run(
                action="setup_dashboard",
                dashboard_type="grafana",
                services=services
            )
            results['dashboard_config'] = dashboard_result
            
            return results
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def optimize_deployment_performance(self, target_environment: str,
                                      optimization_areas: List[str] = None) -> Dict[str, Any]:
        """优化部署性能"""
        try:
            optimization_areas = optimization_areas or [
                "container_optimization", "resource_allocation", 
                "caching_strategy", "database_tuning"
            ]
            
            optimizations = {
                'container_optimization': """
🚀 容器性能优化:

1. 镜像优化:
   - 使用多阶段构建减少镜像大小
   - 选择合适的基础镜像(Alpine vs Debian)
   - 清理不必要的包和缓存
   - 使用.dockerignore减少构建上下文

2. 运行时优化:
   - 配置合适的资源限制(CPU/Memory)
   - 启用健康检查和就绪探针
   - 优化启动时间和优雅关闭
   - 使用非root用户运行容器

3. 网络优化:
   - 配置容器网络策略
   - 启用网络缓存和压缩
   - 优化负载均衡配置
   - 减少容器间网络延迟
""",
                'resource_allocation': """
⚙️ 资源分配优化:

1. CPU优化:
   - 根据应用特性分配CPU资源
   - 启用CPU亲和性绑定
   - 配置合适的CPU限制和请求
   - 监控CPU使用率和调整

2. 内存管理:
   - 设置合理的内存限制
   - 启用内存使用监控
   - 配置OOM策略
   - 优化JVM/Python内存设置

3. 存储优化:
   - 选择合适的存储类型
   - 配置存储卷挂载策略
   - 启用存储监控和告警
   - 优化数据库存储配置
""",
                'caching_strategy': """
🗄️ 缓存策略优化:

1. 应用层缓存:
   - Redis缓存配置优化
   - 缓存失效策略设计
   - 缓存预热和更新机制
   - 分布式缓存一致性

2. CDN和静态资源:
   - 配置CDN加速
   - 静态资源缓存策略
   - 浏览器缓存优化
   - 图片和媒体文件优化

3. 数据库缓存:
   - 查询结果缓存
   - 连接池优化
   - 读写分离配置
   - 索引优化建议
""",
                'database_tuning': """
🗃️ 数据库性能调优:

1. PostgreSQL优化:
   - 连接池配置(max_connections)
   - 内存参数调优(shared_buffers, work_mem)
   - 查询优化器配置
   - 索引策略和维护

2. Redis配置:
   - 内存使用策略
   - 持久化配置优化
   - 主从复制设置
   - 集群模式配置

3. 监控和诊断:
   - 慢查询日志分析
   - 性能指标监控
   - 瓶颈识别和优化
   - 容量规划建议
"""
            }
            
            results = {
                'optimization_plan': [],
                'recommendations': {},
                'implementation_steps': [],
                'monitoring_metrics': [],
                'status': 'success'
            }
            
            for area in optimization_areas:
                if area in optimizations:
                    results['recommendations'][area] = optimizations[area]
                    results['optimization_plan'].append(f"✅ {area} 优化方案已生成")
            
            # 添加实施步骤
            results['implementation_steps'] = [
                "1. 分析当前性能基线和瓶颈",
                "2. 按优先级实施优化措施",
                "3. 监控优化效果和性能指标",
                "4. 持续调优和性能测试",
                "5. 建立性能监控和告警机制"
            ]
            
            # 添加关键监控指标
            results['monitoring_metrics'] = [
                "📊 应用响应时间 (P95/P99)",
                "🔄 请求吞吐量 (RPS)",
                "💾 内存使用率和垃圾回收",
                "🏗️ CPU使用率和负载",
                "🗄️ 数据库连接数和查询时间",
                "📶 缓存命中率和性能",
                "🌐 网络延迟和带宽使用"
            ]
            
            return results
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def create_disaster_recovery_plan(self, services: List[str],
                                    recovery_objectives: Dict[str, str] = None) -> Dict[str, Any]:
        """创建灾难恢复计划"""
        try:
            recovery_objectives = recovery_objectives or {
                "RTO": "30分钟",  # Recovery Time Objective
                "RPO": "5分钟"    # Recovery Point Objective
            }
            
            dr_plan = {
                'backup_strategy': f"""
💾 备份策略设计:

🎯 恢复目标:
- RTO (恢复时间目标): {recovery_objectives.get('RTO', '30分钟')}
- RPO (恢复点目标): {recovery_objectives.get('RPO', '5分钟')}

📋 备份范围:
""",
                'recovery_procedures': """
🔧 恢复流程:

1. 紧急响应阶段:
   - 问题检测和告警响应
   - 影响评估和决策制定
   - 启动灾难恢复流程
   - 通知相关人员和用户

2. 系统恢复阶段:
   - 基础设施恢复或切换
   - 数据恢复和一致性检查
   - 应用服务启动和验证
   - 网络和安全配置恢复

3. 业务恢复阶段:
   - 业务功能验证测试
   - 数据完整性检查
   - 用户访问恢复
   - 性能监控和调优

4. 恢复后处理:
   - 根因分析和总结
   - 流程改进和优化
   - 文档更新和培训
   - 下次演练计划制定
""",
                'monitoring_alerts': """
🚨 监控和告警配置:

⚡ 关键告警指标:
- 服务可用性监控 (>99.9%)
- 数据库连接状态
- 存储空间使用率 (<80%)
- 网络连通性检查
- 安全事件检测

📱 告警通知渠道:
- 即时通知: Slack/钉钉/短信
- 邮件汇总: 每小时状态报告
- 电话告警: 严重故障升级
- 移动应用: 推送通知

🔄 自动化响应:
- 自动故障转移
- 服务自动重启
- 扩容和负载调整
- 备份任务触发
""",
                'testing_schedule': """
🧪 灾难恢复演练:

📅 演练计划:
- 月度演练: 单组件故障恢复
- 季度演练: 多服务故障模拟
- 年度演练: 全系统灾难恢复
- 不定期: 随机故障注入测试

✅ 演练验证点:
- 备份恢复完整性
- 恢复时间符合RTO目标
- 数据丢失符合RPO要求
- 业务功能正常运行
- 团队响应流程顺畅

📊 演练报告:
- 演练过程记录
- 发现问题和改进点
- 恢复时间统计
- 流程优化建议
"""
            }
            
            # 为每个服务添加具体的备份配置
            for service in services:
                if service == "db":
                    dr_plan['backup_strategy'] += """
  📊 数据库备份:
    - 全量备份: 每日凌晨自动执行
    - 增量备份: 每小时WAL归档
    - 异地备份: 跨可用区复制
    - 备份验证: 定期恢复测试
"""
                elif service == "redis":
                    dr_plan['backup_strategy'] += """
  🗄️ Redis缓存备份:
    - RDB快照: 每6小时生成
    - AOF日志: 实时持久化
    - 主从复制: 实时数据同步
    - 集群备份: 多节点冗余
"""
                elif service == "backend":
                    dr_plan['backup_strategy'] += """
  🚀 应用服务备份:
    - 容器镜像: 版本化存储
    - 配置文件: Git版本控制
    - 应用数据: 定期导出
    - 日志备份: 长期存档
"""
            
            return {
                'disaster_recovery_plan': dr_plan,
                'implementation_timeline': [
                    "第1周: 备份策略实施",
                    "第2周: 监控告警配置",
                    "第3周: 恢复流程测试",
                    "第4周: 团队培训和演练"
                ],
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def health_check(self) -> Dict[str, Any]:
        """DeploymentAgent健康检查"""
        try:
            health_status = {
                'agent_status': '✅ 运行正常',
                'tools_status': {},
                'capabilities': [
                    '🐳 Docker容器化管理',
                    '🚀 CI/CD流水线设计',
                    '🏗️ 多环境配置管理',
                    '📊 监控和告警设置',
                    '⚡ 性能优化建议',
                    '💾 灾难恢复规划'
                ],
                'integration_status': {
                    'task_coordinator': '✅ 已集成',
                    'backend_agent': '✅ 协同工作',
                    'test_agent': '✅ 部署验证集成'
                }
            }
            
            # 检查各个工具的状态
            for tool in self.tools:
                try:
                    tool_name = tool.name
                    health_status['tools_status'][tool_name] = '✅ 可用'
                except Exception as e:
                    health_status['tools_status'][tool_name] = f'❌ 异常: {str(e)}'
            
            return health_status
            
        except Exception as e:
            return {
                'agent_status': '❌ 异常',
                'error': str(e)
            }


# 创建全局部署Agent实例
deployment_agent = DeploymentAgent()


# 便捷函数
def containerize_app(services: List[str], environment: str = "production") -> Dict[str, Any]:
    """容器化应用的便捷函数"""
    return deployment_agent.containerize_application(services, environment)


def setup_pipeline(platform: str = "github", features: List[str] = None) -> Dict[str, Any]:
    """设置CI/CD流水线的便捷函数"""
    return deployment_agent.setup_cicd_pipeline(platform, features)


def configure_envs(environments: List[str]) -> Dict[str, Any]:
    """配置多环境的便捷函数"""
    return deployment_agent.configure_environments(environments)


def setup_monitoring(services: List[str], stack: str = "prometheus") -> Dict[str, Any]:
    """设置监控的便捷函数"""
    return deployment_agent.setup_monitoring_stack(services, stack)


def optimize_performance(environment: str, areas: List[str] = None) -> Dict[str, Any]:
    """性能优化的便捷函数"""
    return deployment_agent.optimize_deployment_performance(environment, areas)


def create_dr_plan(services: List[str], objectives: Dict[str, str] = None) -> Dict[str, Any]:
    """创建灾难恢复计划的便捷函数"""
    return deployment_agent.create_disaster_recovery_plan(services, objectives)


def check_deployment_health() -> Dict[str, Any]:
    """检查部署Agent健康状态的便捷函数"""
    return deployment_agent.health_check()