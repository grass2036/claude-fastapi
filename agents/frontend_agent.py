"""
前端开发专家Agent
专门负责Vue.js应用开发、UI设计、组件生成和用户体验优化
"""

from crewai import Agent, Task, Crew, Process
from .tools import (
    DocumentationGenerationTool,
    CodeAnalysisTool,
    ProjectStructureTool,
    HealthCheckTool
)
from .frontend_tools import (
    VueComponentGeneratorTool,
    UIDesignTool,
    VuetifyComponentTool,
    ResponsiveDesignTool,
    FrontendAnalysisTool
)


class FrontendDeveloperAgent:
    """前端开发专家Agent类"""
    
    def __init__(self):
        self.tools = [
            VueComponentGeneratorTool(),
            UIDesignTool(),
            VuetifyComponentTool(),
            ResponsiveDesignTool(),
            FrontendAnalysisTool(),
            DocumentationGenerationTool(),
            CodeAnalysisTool(),
            ProjectStructureTool(),
            HealthCheckTool()
        ]
        
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """创建前端开发专家Agent"""
        return Agent(
            role='Frontend Development & UI Design Specialist',
            goal='设计和开发现代化、用户友好的Vue.js前端应用，提供卓越的用户体验',
            backstory="""
            你是一位资深的前端开发和UI设计专家，拥有丰富的现代化Web应用开发经验。
            你的专长包括：
            
            🎨 **UI/UX设计核心技能**:
            - Material Design 3.0设计规范
            - 响应式设计和移动端适配
            - 用户体验优化和可用性设计
            - 色彩搭配和视觉层次设计
            - 交互动画和过渡效果设计
            - 无障碍设计(A11y)最佳实践
            
            💻 **前端技术专精**:
            - Vue.js 3 Composition API
            - Vuetify 3 组件库深度应用
            - Vue Router 4 路由设计
            - Vuex 4 状态管理架构
            - TypeScript 类型安全开发
            - Vite 构建优化配置
            
            🎯 **核心设计原则**:
            - 用户体验至上(UX First)
            - 移动端优先设计(Mobile First)
            - 渐进式增强(Progressive Enhancement)
            - 性能优化导向(Performance Oriented)
            - 可访问性友好(Accessibility Friendly)
            - 组件化和可复用设计
            
            🚀 **专业特长**:
            - 擅长将复杂的业务逻辑转化为直观的用户界面
            - 能够快速原型设计和迭代优化
            - 精通现代化CSS技术(Flexbox、Grid、CSS变量)
            - 熟悉前端性能优化和SEO最佳实践
            - 具备跨浏览器兼容性解决经验
            
            你的目标是创建既美观又实用的前端应用，让每个用户都能获得流畅、直观的使用体验。
            """,
            tools=self.tools,
            verbose=True,
            allow_delegation=False,
            max_iter=5
        )
    
    def generate_vue_component(self, component_name: str, requirements: str) -> str:
        """生成Vue组件"""
        task = Task(
            description=f"""
            为项目生成 {component_name} Vue组件。
            
            **需求描述**: {requirements}
            
            **技术要求**:
            1. 使用Vue 3 Composition API
            2. 集成Vuetify 3组件
            3. 支持响应式设计
            4. 包含TypeScript类型定义
            5. 遵循项目代码规范
            6. 包含必要的props和events
            7. 添加适当的样式和动画
            8. 考虑无障碍设计(a11y)
            
            **输出格式**:
            - 完整的.vue文件代码
            - 组件使用示例
            - 属性和方法说明
            - 样式变量定义
            """,
            agent=self.agent,
            expected_output="完整的Vue组件代码，包含模板、脚本、样式和使用文档"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def design_ui_layout(self, page_name: str, business_requirements: str) -> str:
        """设计UI页面布局"""
        task = Task(
            description=f"""
            为 {page_name} 页面设计现代化UI布局。
            
            **业务需求**: {business_requirements}
            
            **设计要求**:
            1. 遵循Material Design 3.0规范
            2. 移动端优先的响应式设计
            3. 清晰的信息架构和视觉层次
            4. 优秀的用户体验和交互设计
            5. 符合项目整体设计风格
            6. 考虑用户的操作流程和习惯
            7. 包含状态管理(加载、错误、空状态)
            8. 支持国际化(i18n)设计
            
            **输出内容**:
            1. 详细的页面布局设计描述
            2. 组件层次结构图
            3. 色彩搭配和字体规范
            4. 交互流程说明
            5. 响应式断点设计
            6. Vuetify组件选择建议
            7. 用户体验改进建议
            """,
            agent=self.agent,
            expected_output="完整的UI设计方案，包含布局、交互、样式和技术实现建议"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def optimize_user_experience(self, page_path: str, issues: str = "") -> str:
        """优化用户体验"""
        task = Task(
            description=f"""
            分析并优化 {page_path} 的用户体验。
            
            **已知问题**: {issues if issues else "进行全面的UX审计"}
            
            **优化领域**:
            1. 🎯 **可用性优化**
               - 导航结构和信息架构
               - 操作流程简化
               - 错误处理和反馈机制
               - 加载状态和性能优化
            
            2. 📱 **响应式体验**
               - 移动端操作体验
               - 触摸友好的交互设计
               - 屏幕适配和布局优化
               - 手势和滑动操作
            
            3. ♿ **可访问性改进**
               - 键盘导航支持
               - 屏幕阅读器兼容
               - 颜色对比度优化
               - 焦点管理和ARIA属性
            
            4. 🚀 **性能优化**
               - 组件懒加载策略
               - 图片优化和CDN使用
               - 代码分割和缓存策略
               - 首屏渲染优化
            
            **输出内容**:
            - UX审计报告和问题分析
            - 具体的改进建议和实施方案
            - 代码修改建议
            - 性能优化策略
            """,
            agent=self.agent,
            expected_output="详细的UX优化报告，包含问题分析、改进方案和实施建议"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def create_component_library(self, component_category: str) -> str:
        """创建组件库"""
        task = Task(
            description=f"""
            为项目创建 {component_category} 类别的组件库。
            
            **组件库要求**:
            1. 🧩 **组件设计原则**
               - 高度可复用和可组合
               - 一致的API设计模式
               - 完整的props和events定义
               - 支持插槽(slots)扩展
            
            2. 📚 **文档化标准**
               - 详细的使用示例
               - API参数说明
               - 样式变量文档
               - 最佳实践指南
            
            3. 🎨 **设计系统集成**
               - 统一的视觉风格
               - 标准化的间距和尺寸
               - 一致的色彩和字体规范
               - 响应式设计支持
            
            4. 🧪 **质量保证**
               - 组件单元测试
               - 可访问性测试
               - 浏览器兼容性验证
               - 性能基准测试
            
            **输出内容**:
            - 组件库架构设计
            - 核心组件实现代码
            - 使用文档和示例
            - 样式指南和设计规范
            - 测试用例和验证方法
            """,
            agent=self.agent,
            expected_output="完整的组件库设计和实现方案，包含代码、文档和测试"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def analyze_frontend_performance(self, target_pages: str = "all") -> str:
        """分析前端性能"""
        task = Task(
            description=f"""
            对前端应用进行全面的性能分析和优化建议。
            
            **分析范围**: {target_pages}
            
            **性能分析维度**:
            1. 🚀 **加载性能**
               - 首屏渲染时间(FCP)
               - 最大内容绘制(LCP)
               - 交互准备时间(TTI)
               - 累积布局偏移(CLS)
            
            2. 📦 **资源优化**
               - JavaScript包大小分析
               - CSS优化和未使用样式清理
               - 图片格式和压缩优化
               - 字体加载优化策略
            
            3. 🔧 **技术优化**
               - Vue组件性能优化
               - 路由懒加载实现
               - 状态管理性能优化
               - API请求优化策略
            
            4. 📱 **用户体验指标**
               - 响应时间和流畅度
               - 内存使用和性能监控
               - 离线功能和PWA特性
               - 错误监控和用户反馈
            
            **优化建议输出**:
            - 详细的性能审计报告
            - 优先级排序的优化建议
            - 具体的代码改进方案
            - 性能监控和测量方法
            - 长期性能改进规划
            """,
            agent=self.agent,
            expected_output="综合的前端性能分析报告和优化实施方案"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
    
    def health_check(self) -> str:
        """检查前端开发Agent健康状态"""
        task = Task(
            description="""
            执行前端开发环境和工具链的健康检查。
            
            **检查项目**:
            1. Vue.js项目配置和依赖
            2. Vuetify组件库集成状态
            3. 前端开发工具可用性
            4. 代码规范和质量工具
            5. 构建和开发服务器状态
            
            **输出要求**:
            - 详细的健康状态报告
            - 发现的问题和解决建议
            - 前端开发环境评估
            - 工具链优化建议
            """,
            agent=self.agent,
            expected_output="前端开发环境健康检查报告，包含状态评估和改进建议"
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()


# 创建全局前端开发Agent实例
frontend_agent = FrontendDeveloperAgent()


# 便捷函数
def generate_vue_component(component_name: str, requirements: str) -> str:
    """生成Vue组件的便捷函数"""
    return frontend_agent.generate_vue_component(component_name, requirements)


def design_ui_layout(page_name: str, business_requirements: str) -> str:
    """设计UI布局的便捷函数"""
    return frontend_agent.design_ui_layout(page_name, business_requirements)


def optimize_ux(page_path: str, issues: str = "") -> str:
    """优化用户体验的便捷函数"""
    return frontend_agent.optimize_user_experience(page_path, issues)


def create_component_library(category: str) -> str:
    """创建组件库的便捷函数"""
    return frontend_agent.create_component_library(category)


def analyze_performance(pages: str = "all") -> str:
    """分析前端性能的便捷函数"""
    return frontend_agent.analyze_frontend_performance(pages)


def check_frontend_health() -> str:
    """检查前端Agent健康状态的便捷函数"""
    return frontend_agent.health_check()