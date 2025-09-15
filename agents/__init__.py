"""
Claude FastAPI Agent系统

这个包包含了为Claude FastAPI项目设计的智能Agent系统，
包括文档生成Agent、前端开发专家Agent和其他专业化的开发助手Agent。

主要功能:
- 自动生成技术文档
- Vue.js组件生成和UI设计
- 用户体验优化
- 代码分析和项目结构分析
- 健康检查和状态监控
- 与Claude Code CLI集成
"""

# 动态导入以处理依赖问题
try:
    from .doc_agent import documentation_agent, generate_docs, analyze_code, check_health
    DOC_AGENT_AVAILABLE = True
except ImportError:
    DOC_AGENT_AVAILABLE = False
    documentation_agent = None
    generate_docs = None
    analyze_code = None
    check_health = None

try:
    from .frontend_agent import (
        frontend_agent,
        generate_vue_component,
        design_ui_layout,
        optimize_ux,
        create_component_library,
        analyze_performance,
        check_frontend_health
    )
    FRONTEND_AGENT_AVAILABLE = True
except ImportError:
    # 使用简化版前端Agent
    from .frontend_agent_simple import (
        frontend_agent_simple as frontend_agent,
        generate_vue_component_simple as generate_vue_component,
        design_ui_layout_simple as design_ui_layout,
        optimize_ux_simple as optimize_ux,
        create_component_library_simple as create_component_library,
        analyze_performance_simple as analyze_performance,
        check_frontend_health_simple as check_frontend_health
    )
    FRONTEND_AGENT_AVAILABLE = True

__all__ = [
    # 文档生成Agent
    "documentation_agent",
    "generate_docs", 
    "analyze_code",
    "check_health",
    
    # 前端开发专家Agent
    "frontend_agent",
    "generate_vue_component",
    "design_ui_layout",
    "optimize_ux", 
    "create_component_library",
    "analyze_performance",
    "check_frontend_health"
]

__version__ = "1.0.0"