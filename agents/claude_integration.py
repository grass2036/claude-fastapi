"""
Claude Code集成工具
提供与Claude Code的无缝集成功能
"""

import subprocess
import json
import os
from typing import Dict, Any, Optional, List
from pathlib import Path


class ClaudeCodeIntegration:
    """Claude Code集成类"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.ensure_project_exists()
    
    def ensure_project_exists(self):
        """确保项目路径存在"""
        if not self.project_path.exists():
            raise FileNotFoundError(f"项目路径不存在: {self.project_path}")
    
    def execute_command(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """执行Claude Code命令"""
        try:
            # 构建命令 - 使用交互式方式
            env = os.environ.copy()
            env['CLAUDE_AUTO_ACCEPT'] = 'true'  # 自动接受建议
            
            # 使用echo传递prompt到claude
            cmd = f'echo "{prompt}" | claude'
            
            # 执行命令
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.project_path,
                env=env,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                error_msg = result.stderr.strip()
                return f"❌ 执行失败: {error_msg}"
                
        except subprocess.TimeoutExpired:
            return "❌ 执行超时 (5分钟)"
        except Exception as e:
            return f"❌ 执行异常: {str(e)}"
    
    def analyze_file(self, file_path: str) -> str:
        """分析指定文件"""
        relative_path = self._get_relative_path(file_path)
        prompt = f"请分析文件 {relative_path} 的内容，包括功能、结构和可能的改进点"
        return self.execute_command(prompt)
    
    def generate_documentation(self, target: str, doc_type: str = "api") -> str:
        """生成文档"""
        prompts = {
            "api": f"为 {target} 生成详细的API文档，包括接口说明、参数、返回值和使用示例",
            "readme": f"为 {target} 生成README.md文档，包括项目介绍、安装指南、使用方法",
            "technical": f"为 {target} 生成技术文档，包括架构设计、实现原理和开发指南",
            "user": f"为 {target} 生成用户文档，包括功能介绍、操作步骤和常见问题"
        }
        
        prompt = prompts.get(doc_type, prompts["api"])
        return self.execute_command(prompt)
    
    def review_code(self, file_path: str) -> str:
        """代码审查"""
        relative_path = self._get_relative_path(file_path)
        prompt = f"""
        请审查文件 {relative_path} 的代码质量，检查以下方面：
        1. 代码规范和风格
        2. 潜在的bug和安全问题
        3. 性能优化建议
        4. 最佳实践建议
        5. 可读性和维护性
        """
        return self.execute_command(prompt)
    
    def explain_code(self, file_path: str) -> str:
        """解释代码功能"""
        relative_path = self._get_relative_path(file_path)
        prompt = f"""
        请详细解释文件 {relative_path} 的功能和实现：
        1. 主要功能和用途
        2. 关键类和方法的作用
        3. 实现逻辑和算法
        4. 与其他模块的关系
        5. 使用示例
        """
        return self.execute_command(prompt)
    
    def get_project_structure(self) -> str:
        """获取项目结构"""
        prompt = "分析并展示项目的目录结构，突出显示主要模块和关键文件"
        return self.execute_command(prompt)
    
    def suggest_improvements(self, target: str) -> str:
        """建议改进"""
        prompt = f"""
        针对 {target} 提供改进建议：
        1. 代码质量提升
        2. 性能优化
        3. 安全性增强
        4. 可维护性改进
        5. 新功能建议
        """
        return self.execute_command(prompt)
    
    def _get_relative_path(self, file_path: str) -> str:
        """获取相对路径"""
        try:
            abs_path = Path(file_path)
            if abs_path.is_absolute():
                return str(abs_path.relative_to(self.project_path))
            return file_path
        except ValueError:
            return file_path
    
    def list_python_files(self) -> List[str]:
        """列出所有Python文件"""
        python_files = []
        for py_file in self.project_path.rglob("*.py"):
            # 排除虚拟环境和缓存目录
            if not any(part.startswith('.') or part == '__pycache__' or part == 'venv' 
                      for part in py_file.parts):
                python_files.append(str(py_file.relative_to(self.project_path)))
        return python_files
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        try:
            # 检查claude命令是否可用
            result = subprocess.run(
                ["claude", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            claude_available = result.returncode == 0
            version = result.stdout.strip() if claude_available else "未安装"
            
            # 检查项目状态
            project_exists = self.project_path.exists()
            python_files_count = len(self.list_python_files()) if project_exists else 0
            
            return {
                "claude_available": claude_available,
                "claude_version": version,
                "project_exists": project_exists,
                "project_path": str(self.project_path),
                "python_files_count": python_files_count,
                "status": "✅ 正常" if claude_available and project_exists else "❌ 异常"
            }
            
        except Exception as e:
            return {
                "claude_available": False,
                "error": str(e),
                "status": "❌ 检查失败"
            }


# 全局实例
claude_integration = ClaudeCodeIntegration("/Users/chiyingjie/code/git/claude-fastapi")