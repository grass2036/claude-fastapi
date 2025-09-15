"""
Agent工具集合
为不同的Agent提供专门的工具
"""

from typing import Type, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

from .claude_integration import claude_integration


class DocumentationGenerationInput(BaseModel):
    """文档生成输入模型"""
    target: str = Field(..., description="目标文件或模块路径")
    doc_type: str = Field(default="api", description="文档类型: api, readme, technical, user")
    include_examples: bool = Field(default=True, description="是否包含使用示例")


class DocumentationGenerationTool(BaseTool):
    """文档生成工具"""
    name: str = "documentation_generator"
    description: str = "生成各种类型的项目文档，包括API文档、README、技术文档等"
    args_schema: Type[BaseModel] = DocumentationGenerationInput
    
    def _run(self, target: str, doc_type: str = "api", include_examples: bool = True) -> str:
        """执行文档生成"""
        try:
            result = claude_integration.generate_documentation(target, doc_type)
            
            if include_examples and doc_type == "api":
                # 为API文档添加使用示例
                example_prompt = f"为 {target} 的API提供详细的使用示例和代码片段"
                examples = claude_integration.execute_command(example_prompt)
                result += f"\n\n## 使用示例\n\n{examples}"
            
            return f"✅ 文档生成完成:\n\n{result}"
            
        except Exception as e:
            return f"❌ 文档生成失败: {str(e)}"


class CodeAnalysisInput(BaseModel):
    """代码分析输入模型"""
    file_path: str = Field(..., description="要分析的文件路径")
    analysis_type: str = Field(default="full", description="分析类型: full, structure, quality")


class CodeAnalysisTool(BaseTool):
    """代码分析工具"""
    name: str = "code_analyzer"
    description: str = "分析代码文件的结构、功能和质量"
    args_schema: Type[BaseModel] = CodeAnalysisInput
    
    def _run(self, file_path: str, analysis_type: str = "full") -> str:
        """执行代码分析"""
        try:
            if analysis_type == "full":
                return claude_integration.analyze_file(file_path)
            elif analysis_type == "structure":
                return claude_integration.explain_code(file_path)
            elif analysis_type == "quality":
                return claude_integration.review_code(file_path)
            else:
                return claude_integration.analyze_file(file_path)
                
        except Exception as e:
            return f"❌ 代码分析失败: {str(e)}"


class ProjectStructureInput(BaseModel):
    """项目结构输入模型"""
    show_details: bool = Field(default=True, description="是否显示详细信息")


class ProjectStructureTool(BaseTool):
    """项目结构分析工具"""
    name: str = "project_structure_analyzer"
    description: str = "分析和展示项目的目录结构和组织方式"
    args_schema: Type[BaseModel] = ProjectStructureInput
    
    def _run(self, show_details: bool = True) -> str:
        """执行项目结构分析"""
        try:
            structure = claude_integration.get_project_structure()
            
            if show_details:
                # 添加Python文件统计
                python_files = claude_integration.list_python_files()
                file_summary = f"\n\n📊 项目统计:\n- Python文件数量: {len(python_files)}"
                
                # 按目录分组
                dirs = {}
                for file in python_files:
                    dir_name = file.split('/')[0] if '/' in file else 'root'
                    dirs[dir_name] = dirs.get(dir_name, 0) + 1
                
                for dir_name, count in dirs.items():
                    file_summary += f"\n- {dir_name}: {count}个文件"
                
                structure += file_summary
            
            return f"📁 项目结构分析:\n\n{structure}"
            
        except Exception as e:
            return f"❌ 项目结构分析失败: {str(e)}"


class ImprovementSuggestionInput(BaseModel):
    """改进建议输入模型"""
    target: str = Field(..., description="目标文件、模块或功能")
    focus_area: str = Field(default="all", description="关注领域: performance, security, maintainability, all")


class ImprovementSuggestionTool(BaseTool):
    """改进建议工具"""
    name: str = "improvement_suggester"
    description: str = "分析代码并提供改进建议"
    args_schema: Type[BaseModel] = ImprovementSuggestionInput
    
    def _run(self, target: str, focus_area: str = "all") -> str:
        """执行改进建议分析"""
        try:
            suggestions = claude_integration.suggest_improvements(target)
            
            if focus_area != "all":
                # 针对特定领域的建议
                focused_prompt = f"""
                针对 {target} 的 {focus_area} 方面提供详细的改进建议：
                包括具体的实施步骤和代码示例
                """
                focused_suggestions = claude_integration.execute_command(focused_prompt)
                suggestions += f"\n\n🎯 {focus_area} 专项建议:\n{focused_suggestions}"
            
            return f"💡 改进建议:\n\n{suggestions}"
            
        except Exception as e:
            return f"❌ 改进建议生成失败: {str(e)}"


class HealthCheckTool(BaseTool):
    """健康检查工具"""
    name: str = "health_checker"
    description: str = "检查Claude Code集成和项目状态"
    
    def _run(self) -> str:
        """执行健康检查"""
        try:
            health_status = claude_integration.health_check()
            
            status_text = f"""
🔍 系统健康检查报告:

Claude Code状态: {'✅ 可用' if health_status['claude_available'] else '❌ 不可用'}
版本信息: {health_status.get('claude_version', 'N/A')}
项目路径: {health_status['project_path']}
项目状态: {'✅ 存在' if health_status['project_exists'] else '❌ 不存在'}
Python文件: {health_status.get('python_files_count', 0)} 个

总体状态: {health_status['status']}
"""
            
            if 'error' in health_status:
                status_text += f"\n❌ 错误信息: {health_status['error']}"
            
            return status_text
            
        except Exception as e:
            return f"❌ 健康检查失败: {str(e)}"


# 导出所有工具
__all__ = [
    "DocumentationGenerationTool",
    "CodeAnalysisTool", 
    "ProjectStructureTool",
    "ImprovementSuggestionTool",
    "HealthCheckTool"
]