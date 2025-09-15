"""
Agent管理器
统一管理和协调所有Agent的工作
"""

from typing import Dict, List, Optional, Any
try:
    from .doc_agent import DocumentationAgent
except ImportError:
    # CrewAI不可用时的回退
    DocumentationAgent = None

try:
    from .frontend_agent import FrontendDeveloperAgent
except ImportError:
    # CrewAI不可用时使用简化版
    from .frontend_agent_simple import FrontendDeveloperAgentSimple as FrontendDeveloperAgent

from .claude_integration import claude_integration


class AgentManager:
    """Agent管理器类，负责协调和管理所有Agent"""
    
    def __init__(self):
        """初始化所有可用的Agent"""
        self.agents = {}
        
        # 初始化文档Agent（如果可用）
        if DocumentationAgent is not None:
            try:
                self.agents['documentation'] = DocumentationAgent()
            except Exception as e:
                print(f"⚠️ 文档Agent初始化失败: {e}")
        
        # 初始化前端Agent
        try:
            self.agents['frontend'] = FrontendDeveloperAgent()
        except Exception as e:
            print(f"⚠️ 前端Agent初始化失败: {e}")
        
    def list_agents(self) -> List[str]:
        """列出所有可用的Agent"""
        return list(self.agents.keys())
    
    def get_agent(self, agent_name: str) -> Optional[Any]:
        """获取指定的Agent实例"""
        return self.agents.get(agent_name)
    
    def execute_task(self, agent_name: str, task_type: str, **kwargs) -> str:
        """执行Agent任务"""
        agent = self.get_agent(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found")
        
        # 根据Agent类型和任务类型分发任务
        if agent_name == 'documentation':
            return self._execute_documentation_task(agent, task_type, **kwargs)
        elif agent_name == 'frontend':
            return self._execute_frontend_task(agent, task_type, **kwargs)
        else:
            raise ValueError(f"Unknown agent type: {agent_name}")
    
    def _execute_documentation_task(self, agent: DocumentationAgent, task_type: str, **kwargs) -> str:
        """执行文档生成Agent任务"""
        if task_type == 'generate_api_doc':
            return agent.generate_api_documentation(
                kwargs.get('target_module', 'backend.api')
            )
        elif task_type == 'generate_tech_doc':
            return agent.generate_technical_documentation(
                kwargs.get('component', 'middleware')
            )
        elif task_type == 'generate_user_guide':
            return agent.generate_user_guide(
                kwargs.get('topic', 'getting_started')
            )
        elif task_type == 'update_readme':
            return agent.update_readme(
                kwargs.get('project_root', '.')
            )
        elif task_type == 'analyze_code':
            return agent.analyze_codebase(
                kwargs.get('target_path', 'backend/')
            )
        elif task_type == 'health_check':
            return agent.health_check()
        else:
            raise ValueError(f"Unknown documentation task: {task_type}")
    
    def _execute_frontend_task(self, agent: FrontendDeveloperAgent, task_type: str, **kwargs) -> str:
        """执行前端开发Agent任务"""
        try:
            if task_type == 'generate_component':
                result = agent.generate_vue_component(
                    kwargs.get('component_name', 'NewComponent'),
                    kwargs.get('requirements', 'Basic Vue component')
                )
            elif task_type == 'design_layout':
                result = agent.design_ui_layout(
                    kwargs.get('page_name', 'HomePage'),
                    kwargs.get('business_requirements', 'User-friendly homepage')
                )
            elif task_type == 'optimize_ux':
                result = agent.optimize_user_experience(
                    kwargs.get('page_path', '/'),
                    kwargs.get('issues', '')
                )
            elif task_type == 'create_component_library':
                result = agent.create_component_library(
                    kwargs.get('component_category', 'common')
                )
            elif task_type == 'analyze_performance':
                result = agent.analyze_frontend_performance(
                    kwargs.get('target_pages', 'all')
                )
            elif task_type == 'health_check':
                result = agent.health_check()
            else:
                raise ValueError(f"Unknown frontend task: {task_type}")
            
            # 处理不同的返回格式（CrewAI vs 简化版）
            if isinstance(result, dict):
                # 简化版返回字典格式
                if result.get('status') == 'success':
                    return f"✅ 任务完成\n\n{result.get('content', str(result))}"
                else:
                    return f"❌ 任务失败: {result.get('error', '未知错误')}"
            else:
                # CrewAI版本返回字符串
                return str(result)
                
        except Exception as e:
            return f"❌ 执行失败: {str(e)}"
    
    def get_agent_capabilities(self, agent_name: str) -> Dict[str, List[str]]:
        """获取Agent的能力列表"""
        capabilities = {
            'documentation': [
                'generate_api_doc',
                'generate_tech_doc', 
                'generate_user_guide',
                'update_readme',
                'analyze_code',
                'health_check'
            ],
            'frontend': [
                'generate_component',
                'design_layout',
                'optimize_ux',
                'create_component_library',
                'analyze_performance',
                'health_check'
            ]
        }
        
        if agent_name in capabilities:
            return {agent_name: capabilities[agent_name]}
        else:
            return capabilities
    
    def system_status(self) -> Dict[str, Any]:
        """获取所有Agent的状态"""
        status = {}
        for name, agent in self.agents.items():
            try:
                # 尝试执行健康检查
                health_result = agent.health_check()
                status[name] = {
                    'status': 'healthy',
                    'details': health_result
                }
            except Exception as e:
                status[name] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return status


# 创建全局Agent管理器实例
agent_manager = AgentManager()


# 便捷函数
def list_available_agents() -> List[str]:
    """列出所有可用的Agent"""
    return agent_manager.list_agents()


def execute_agent_task(agent_name: str, task_type: str, **kwargs) -> str:
    """执行Agent任务的便捷函数"""
    return agent_manager.execute_task(agent_name, task_type, **kwargs)


def get_system_status() -> Dict[str, Any]:
    """获取系统状态的便捷函数"""
    return agent_manager.system_status()


def get_agent_help(agent_name: Optional[str] = None) -> Dict[str, List[str]]:
    """获取Agent帮助信息"""
    return agent_manager.get_agent_capabilities(agent_name)