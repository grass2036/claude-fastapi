"""
文档生成Agent
专门负责项目文档的生成、维护和更新
"""

from crewai import Agent, Task, Crew, Process
from .tools import (
    DocumentationGenerationTool,
    CodeAnalysisTool,
    ProjectStructureTool,
    ImprovementSuggestionTool,
    HealthCheckTool
)


class DocumentationAgent:
    """文档生成Agent类"""
    
    def __init__(self):
        self.tools = [
            DocumentationGenerationTool(),
            CodeAnalysisTool(),
            ProjectStructureTool(), 
            ImprovementSuggestionTool(),
            HealthCheckTool()
        ]
        
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """创建文档专家Agent"""
        return Agent(
            role='Documentation Specialist',
            goal='生成高质量的项目文档，包括API文档、技术文档、用户指南等',
            backstory="""
            你是一位资深的技术文档专家，拥有丰富的软件项目文档编写经验。
            你的专长包括：
            
            📝 **核心技能**:
            - API文档编写 (OpenAPI/Swagger风格)
            - 技术架构文档
            - 用户操作指南
            - 代码注释和内联文档
            - README和项目介绍
            
            🎯 **工作原则**:
            - 文档内容准确、清晰、易懂
            - 提供丰富的代码示例
            - 考虑不同技术水平的读者
            - 保持文档的时效性和一致性
            - 遵循行业标准和最佳实践
            
            💡 **特殊技能**:
            - 能够理解复杂的代码逻辑并用简单语言解释
            - 擅长创建图表和流程图辅助说明
            - 熟悉各种文档格式 (Markdown, reStructuredText, HTML)
            - 了解FastAPI、Vue.js等现代技术栈
            
            你的目标是帮助开发者和用户更好地理解和使用项目。
            """,
            tools=self.tools,
            verbose=True,
            allow_delegation=False,
            max_iter=3
        )
    
    def generate_api_documentation(self, target_module: str) -> str:
        """生成API文档"""
        task = Task(
            description=f"""
            为 {target_module} 生成完整的API文档。
            
            **任务要求**:
            1. 分析目标模块的代码结构和功能
            2. 生成详细的API接口文档
            3. 包含请求/响应格式说明
            4. 提供实际的使用示例
            5. 添加错误码和处理说明
            6. 确保文档格式规范和易读性
            
            **输出格式**: Markdown格式的API文档
            **示例数量**: 至少3个实际使用场景
            """,
            agent=self.agent,
            expected_output="完整的API文档，包含接口说明、参数、返回值、使用示例和错误处理"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def generate_technical_documentation(self, component: str) -> str:
        """生成技术文档"""
        task = Task(
            description=f"""
            为 {component} 组件生成技术文档。
            
            **文档内容应包括**:
            1. 📋 组件概述和主要功能
            2. 🏗️ 架构设计和实现原理
            3. 🔧 配置和初始化方法
            4. 💻 代码结构和关键类/方法说明
            5. 🔗 与其他组件的集成方式
            6. ⚡ 性能特性和优化建议
            7. 🛠️ 调试和故障排除指南
            8. 📈 扩展和定制方法
            
            **目标读者**: 开发人员和系统架构师
            **深度要求**: 深入技术细节，包含实现逻辑
            """,
            agent=self.agent,
            expected_output="深入的技术文档，涵盖架构设计、实现细节和使用指南"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def generate_user_guide(self, feature: str) -> str:
        """生成用户指南"""
        task = Task(
            description=f"""
            为 {feature} 功能生成用户操作指南。
            
            **指南内容**:
            1. 🎯 功能介绍和使用场景
            2. 🚀 快速开始指南
            3. 📖 详细操作步骤
            4. 💡 最佳实践和使用技巧
            5. ❓ 常见问题和解决方案
            6. ⚠️ 注意事项和限制说明
            7. 🔧 配置选项说明
            8. 📞 支持和反馈渠道
            
            **写作风格**:
            - 简洁明了，避免技术术语
            - 分步骤说明，易于跟随
            - 提供截图或示例（如适用）
            - 考虑不同用户的技术水平
            """,
            agent=self.agent,
            expected_output="用户友好的操作指南，包含清晰的步骤说明和实用建议"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def generate_readme(self, project_focus: str = "overview") -> str:
        """生成README文档"""
        task = Task(
            description=f"""
            为项目生成README.md文档，重点关注 {project_focus}。
            
            **README结构**:
            1. 📄 项目标题和简介
            2. ✨ 主要特性和亮点
            3. 🚀 快速开始指南
            4. 📦 安装和部署说明
            5. 💻 基本使用示例
            6. 📚 文档链接和资源
            7. 🤝 贡献指南
            8. 📄 许可证信息
            9. 📞 联系方式和支持
            
            **特殊要求**:
            - 添加项目徽章和状态指示
            - 包含架构图或流程图描述
            - 提供在线演示链接（如果有）
            - 突出项目的独特价值
            - 适合不同背景的读者
            """,
            agent=self.agent,
            expected_output="专业的README文档，包含项目介绍、安装指南和使用说明"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def analyze_and_document(self, target: str) -> str:
        """分析代码并生成文档"""
        task = Task(
            description=f"""
            对 {target} 进行全面分析并生成综合文档。
            
            **分析任务**:
            1. 🔍 代码结构和功能分析
            2. 📊 复杂度和质量评估
            3. 🔗 依赖关系梳理
            4. 💡 改进建议总结
            
            **文档输出**:
            1. 📋 功能概述和用途说明
            2. 🏗️ 技术实现分析
            3. 📖 使用方法和示例
            4. ⚠️ 注意事项和最佳实践
            5. 🚀 性能特性和优化建议
            6. 🔧 配置和定制选项
            
            **质量标准**:
            - 信息准确、完整
            - 逻辑清晰、结构合理
            - 代码示例可运行
            - 适合目标读者群体
            """,
            agent=self.agent,
            expected_output="基于代码分析的综合文档，包含功能说明、技术细节和使用指南"
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
            执行系统健康检查，确保文档生成环境正常。
            
            **检查项目**:
            1. Claude Code集成状态
            2. 项目文件访问权限
            3. 工具可用性验证
            4. 配置正确性检查
            
            **输出要求**:
            - 详细的状态报告
            - 发现的问题和解决建议
            - 系统性能和可用性评估
            """,
            agent=self.agent,
            expected_output="系统健康检查报告，包含状态评估和改进建议"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()


# 创建全局文档Agent实例
doc_agent = DocumentationAgent()


# 便捷函数
def generate_api_docs(module: str) -> str:
    """生成API文档的便捷函数"""
    return doc_agent.generate_api_documentation(module)


def generate_tech_docs(component: str) -> str:
    """生成技术文档的便捷函数"""
    return doc_agent.generate_technical_documentation(component)


def generate_user_guide(feature: str) -> str:
    """生成用户指南的便捷函数"""
    return doc_agent.generate_user_guide(feature)


def generate_readme(focus: str = "overview") -> str:
    """生成README的便捷函数"""
    return doc_agent.generate_readme(focus)


def analyze_and_document(target: str) -> str:
    """分析并生成文档的便捷函数"""
    return doc_agent.analyze_and_document(target)


def check_doc_agent_health() -> str:
    """检查文档Agent健康状态的便捷函数"""
    return doc_agent.health_check()