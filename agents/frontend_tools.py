"""
前端开发专用工具集合
为前端开发和UI设计Agent提供专门的工具
"""

from typing import Type, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import os
import json
from pathlib import Path

from .claude_integration import claude_integration


class VueComponentInput(BaseModel):
    """Vue组件生成输入模型"""
    component_name: str = Field(..., description="组件名称，如 'UserCard', 'DataTable'")
    component_type: str = Field(default="functional", description="组件类型: functional, form, display, layout")
    props_definition: str = Field(default="", description="组件props定义和说明")
    features: str = Field(default="", description="特殊功能需求，如动画、验证、响应式等")


class VueComponentGeneratorTool(BaseTool):
    """Vue组件代码生成工具"""
    name: str = "vue_component_generator"
    description: str = "生成现代化的Vue 3组件，支持Composition API、TypeScript、Vuetify集成"
    args_schema: Type[BaseModel] = VueComponentInput
    
    def _run(self, component_name: str, component_type: str = "functional", 
             props_definition: str = "", features: str = "") -> str:
        """生成Vue组件代码"""
        try:
            prompt = f"""
            为Vue 3 + Vuetify 3项目生成 {component_name} 组件。

            组件规格:
            - 组件名称: {component_name}
            - 组件类型: {component_type}
            - Props定义: {props_definition}
            - 特殊功能: {features}

            技术要求:
            1. 使用Vue 3 Composition API
            2. 集成Vuetify 3组件和样式
            3. 支持TypeScript类型定义
            4. 响应式设计(移动端友好)
            5. 无障碍设计(aria属性)
            6. 包含适当的过渡动画
            7. 遵循Vue 3最佳实践

            输出格式:
            ```vue
            <template>
              <!-- 组件模板 -->
            </template>

            <script setup lang="ts">
              // 组件逻辑
            </script>

            <style scoped>
              /* 组件样式 */
            </style>
            ```

            还需要包含:
            - 组件使用示例
            - Props和Events文档
            - 样式变量说明
            """
            
            result = claude_integration.execute_command(prompt)
            
            # 保存组件到frontend/src/components/generated/
            self._save_component(component_name, result)
            
            return f"✅ Vue组件生成完成:\n\n{result}"
            
        except Exception as e:
            return f"❌ Vue组件生成失败: {str(e)}"
    
    def _save_component(self, component_name: str, component_code: str):
        """保存生成的组件到文件系统"""
        try:
            # 确保目录存在
            component_dir = Path("frontend/src/components/generated")
            component_dir.mkdir(parents=True, exist_ok=True)
            
            # 提取Vue文件内容（去除markdown代码块标记）
            if "```vue" in component_code:
                start = component_code.find("```vue") + 6
                end = component_code.find("```", start)
                vue_content = component_code[start:end].strip()
            else:
                vue_content = component_code
            
            # 保存文件
            file_path = component_dir / f"{component_name}.vue"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(vue_content)
                
            print(f"📁 组件已保存到: {file_path}")
            
        except Exception as e:
            print(f"⚠️ 组件保存失败: {e}")


class UIDesignInput(BaseModel):
    """UI设计输入模型"""
    design_target: str = Field(..., description="设计目标，如 '登录页面', '数据仪表板', '用户列表'")
    design_style: str = Field(default="modern", description="设计风格: modern, minimal, corporate, creative")
    color_scheme: str = Field(default="blue", description="主色调: blue, green, purple, orange, neutral")
    layout_type: str = Field(default="responsive", description="布局类型: responsive, mobile-first, desktop")


class UIDesignTool(BaseTool):
    """UI设计方案生成工具"""
    name: str = "ui_design_generator"
    description: str = "基于Material Design 3.0生成现代化UI设计方案和样式指南"
    args_schema: Type[BaseModel] = UIDesignInput
    
    def _run(self, design_target: str, design_style: str = "modern", 
             color_scheme: str = "blue", layout_type: str = "responsive") -> str:
        """生成UI设计方案"""
        try:
            prompt = f"""
            为{design_target}设计现代化的UI界面方案。

            设计参数:
            - 设计目标: {design_target}
            - 设计风格: {design_style}
            - 配色方案: {color_scheme}
            - 布局类型: {layout_type}

            请提供详细的设计方案，包括:

            1. 🎨 视觉设计规范
               - 主色调和辅助色彩定义
               - 字体层级和大小规范
               - 间距和边距系统
               - 圆角和阴影规范

            2. 📱 布局结构设计
               - 页面整体布局架构
               - 响应式断点设计
               - 组件层次关系
               - 信息架构和导航

            3. 🧩 Vuetify组件选择
               - 推荐使用的Vuetify组件
               - 组件配置和属性建议
               - 自定义样式需求
               - 主题配置建议

            4. 💡 用户体验设计
               - 交互流程设计
               - 状态反馈和错误处理
               - 加载状态和过渡动画
               - 无障碍设计考虑

            5. 📋 实现指南
               - CSS变量定义
               - 样式实现建议
               - 响应式媒体查询
               - 性能优化建议

            以Markdown格式输出，包含具体的代码示例和配置。
            """
            
            result = claude_integration.execute_command(prompt)
            
            # 保存设计文档
            self._save_design_doc(design_target, result)
            
            return f"✅ UI设计方案生成完成:\n\n{result}"
            
        except Exception as e:
            return f"❌ UI设计方案生成失败: {str(e)}"
    
    def _save_design_doc(self, design_target: str, design_content: str):
        """保存设计文档"""
        try:
            # 确保目录存在
            design_dir = Path("frontend/design-system")
            design_dir.mkdir(parents=True, exist_ok=True)
            
            # 保存设计文档
            safe_name = design_target.replace(" ", "-").replace("/", "-").lower()
            file_path = design_dir / f"{safe_name}-design.md"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(design_content)
                
            print(f"📋 设计文档已保存到: {file_path}")
            
        except Exception as e:
            print(f"⚠️ 设计文档保存失败: {e}")


class VuetifyComponentInput(BaseModel):
    """Vuetify组件定制输入模型"""
    base_component: str = Field(..., description="基础Vuetify组件名，如 'v-card', 'v-data-table'")
    customization_needs: str = Field(..., description="定制需求描述")
    theme_integration: bool = Field(default=True, description="是否集成项目主题")


class VuetifyComponentTool(BaseTool):
    """Vuetify组件定制工具"""
    name: str = "vuetify_component_customizer"
    description: str = "基于Vuetify组件进行定制开发，集成项目设计系统"
    args_schema: Type[BaseModel] = VuetifyComponentInput
    
    def _run(self, base_component: str, customization_needs: str, 
             theme_integration: bool = True) -> str:
        """定制Vuetify组件"""
        try:
            prompt = f"""
            基于Vuetify 3组件 {base_component} 进行定制开发。

            定制要求:
            - 基础组件: {base_component}
            - 定制需求: {customization_needs}
            - 主题集成: {"是" if theme_integration else "否"}

            请提供:
            1. 定制后的Vue组件代码
            2. 样式重写和扩展
            3. 主题变量集成方案
            4. 使用示例和最佳实践
            5. 响应式设计适配

            技术要求:
            - 保持Vuetify组件的原有功能
            - 扩展和增强用户体验
            - 符合Material Design 3规范
            - 支持深色/浅色主题切换
            - 包含完整的TypeScript类型支持

            输出格式应包含完整的Vue组件代码和使用说明。
            """
            
            result = claude_integration.execute_command(prompt)
            return f"✅ Vuetify组件定制完成:\n\n{result}"
            
        except Exception as e:
            return f"❌ Vuetify组件定制失败: {str(e)}"


class ResponsiveDesignInput(BaseModel):
    """响应式设计输入模型"""
    target_component: str = Field(..., description="目标组件或页面名称")
    breakpoints: str = Field(default="mobile,tablet,desktop", description="需要适配的断点")
    priority_device: str = Field(default="mobile", description="优先设备类型")


class ResponsiveDesignTool(BaseTool):
    """响应式设计优化工具"""
    name: str = "responsive_design_optimizer"
    description: str = "优化组件和页面的响应式设计，确保跨设备兼容性"
    args_schema: Type[BaseModel] = ResponsiveDesignInput
    
    def _run(self, target_component: str, breakpoints: str = "mobile,tablet,desktop",
             priority_device: str = "mobile") -> str:
        """优化响应式设计"""
        try:
            prompt = f"""
            为 {target_component} 优化响应式设计。

            设计参数:
            - 目标组件: {target_component}
            - 断点设备: {breakpoints}
            - 优先设备: {priority_device}

            请提供详细的响应式优化方案:

            1. 📱 移动端优化 (320px - 768px)
               - 触摸友好的交互设计
               - 紧凑的布局和导航
               - 优化的字体和间距
               - 手势操作支持

            2. 📟 平板端适配 (768px - 1024px)
               - 中等屏幕布局优化
               - 导航和侧边栏设计
               - 内容密度平衡
               - 横竖屏适配

            3. 🖥️ 桌面端体验 (1024px+)
               - 大屏幕空间利用
               - 多列布局和信息密度
               - 鼠标交互优化
               - 快捷键和高级功能

            4. 🎨 设计技术实现
               - CSS Grid和Flexbox布局
               - 媒体查询断点策略
               - 流体布局和弹性设计
               - 图片和媒体响应式处理

            5. ⚡ 性能考虑
               - 图片懒加载和优化
               - 代码分割和按需加载
               - CSS优化和压缩
               - 移动端性能优化

            输出应包含具体的CSS代码和Vue组件实现示例。
            """
            
            result = claude_integration.execute_command(prompt)
            return f"✅ 响应式设计优化完成:\n\n{result}"
            
        except Exception as e:
            return f"❌ 响应式设计优化失败: {str(e)}"


class FrontendAnalysisInput(BaseModel):
    """前端分析输入模型"""
    analysis_type: str = Field(..., description="分析类型: performance, accessibility, seo, code-quality")
    target_path: str = Field(default="frontend/src", description="分析目标路径")
    focus_areas: str = Field(default="", description="重点关注的领域")


class FrontendAnalysisTool(BaseTool):
    """前端项目分析工具"""
    name: str = "frontend_project_analyzer"
    description: str = "分析前端项目的性能、可访问性、SEO和代码质量"
    args_schema: Type[BaseModel] = FrontendAnalysisInput
    
    def _run(self, analysis_type: str, target_path: str = "frontend/src",
             focus_areas: str = "") -> str:
        """分析前端项目"""
        try:
            # 获取前端项目信息
            frontend_info = self._analyze_frontend_structure(target_path)
            
            prompt = f"""
            对前端项目进行 {analysis_type} 分析。

            项目信息:
            {frontend_info}

            分析类型: {analysis_type}
            目标路径: {target_path}
            关注领域: {focus_areas}

            请根据分析类型提供详细报告:

            {self._get_analysis_prompt(analysis_type)}

            输出格式:
            - 问题识别和严重程度分级
            - 具体的改进建议和实施方案
            - 代码示例和最佳实践
            - 工具推荐和配置指南
            - 长期改进规划
            """
            
            result = claude_integration.execute_command(prompt)
            
            # 保存分析报告
            self._save_analysis_report(analysis_type, result)
            
            return f"✅ {analysis_type}分析完成:\n\n{result}"
            
        except Exception as e:
            return f"❌ 前端项目分析失败: {str(e)}"
    
    def _analyze_frontend_structure(self, target_path: str) -> str:
        """分析前端项目结构"""
        try:
            structure_info = []
            
            # 读取package.json
            package_json_path = Path("frontend/package.json")
            if package_json_path.exists():
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                    structure_info.append(f"依赖: {', '.join(package_data.get('dependencies', {}).keys())}")
            
            # 分析目录结构
            frontend_path = Path(target_path)
            if frontend_path.exists():
                dirs = [d.name for d in frontend_path.iterdir() if d.is_dir()]
                structure_info.append(f"目录结构: {', '.join(dirs)}")
                
                # 统计文件数量
                vue_files = list(frontend_path.rglob("*.vue"))
                js_files = list(frontend_path.rglob("*.js")) + list(frontend_path.rglob("*.ts"))
                structure_info.append(f"Vue组件: {len(vue_files)}个")
                structure_info.append(f"JS/TS文件: {len(js_files)}个")
            
            return "\n".join(structure_info)
            
        except Exception as e:
            return f"项目结构分析失败: {e}"
    
    def _get_analysis_prompt(self, analysis_type: str) -> str:
        """获取特定分析类型的提示"""
        prompts = {
            "performance": """
            性能分析重点:
            1. 包大小和代码分割分析
            2. 组件渲染性能评估
            3. 资源加载优化建议
            4. Core Web Vitals指标优化
            5. 内存使用和性能监控
            """,
            "accessibility": """
            可访问性分析重点:
            1. ARIA属性和语义化HTML
            2. 键盘导航和焦点管理
            3. 颜色对比度和视觉设计
            4. 屏幕阅读器兼容性
            5. WCAG 2.1 AA标准符合性
            """,
            "seo": """
            SEO分析重点:
            1. 页面标题和meta标签优化
            2. 结构化数据和语义化标记
            3. 页面加载性能和Core Web Vitals
            4. 移动端友好性和响应式设计
            5. 内容质量和用户体验
            """,
            "code-quality": """
            代码质量分析重点:
            1. Vue组件设计模式和最佳实践
            2. TypeScript类型安全性
            3. 代码复用性和模块化程度
            4. 错误处理和边界情况
            5. 测试覆盖率和质量保证
            """
        }
        return prompts.get(analysis_type, "通用项目分析")
    
    def _save_analysis_report(self, analysis_type: str, report_content: str):
        """保存分析报告"""
        try:
            # 确保目录存在
            reports_dir = Path("frontend/analysis-reports")
            reports_dir.mkdir(parents=True, exist_ok=True)
            
            # 保存报告
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = reports_dir / f"{analysis_type}_report_{timestamp}.md"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {analysis_type.upper()} 分析报告\n\n")
                f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(report_content)
                
            print(f"📊 分析报告已保存到: {file_path}")
            
        except Exception as e:
            print(f"⚠️ 分析报告保存失败: {e}")


# 导出所有前端工具
__all__ = [
    "VueComponentGeneratorTool",
    "UIDesignTool",
    "VuetifyComponentTool",
    "ResponsiveDesignTool",
    "FrontendAnalysisTool"
]