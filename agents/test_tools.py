"""
测试专用工具集
为测试Agent提供专门的测试生成和管理工具
"""

import os
import re
import ast
from typing import Type, Any, Dict, List, Optional
from pathlib import Path
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

from .claude_integration import claude_integration


class UnitTestGenerationInput(BaseModel):
    """单元测试生成输入模型"""
    source_file: str = Field(..., description="源代码文件路径")
    target_class: Optional[str] = Field(default=None, description="目标测试类名")
    test_type: str = Field(default="unit", description="测试类型: unit, integration, api")
    include_mocks: bool = Field(default=True, description="是否包含Mock对象")
    test_coverage: str = Field(default="basic", description="测试覆盖度: basic, comprehensive")


class UnitTestGenerationTool(BaseTool):
    """pytest单元测试生成工具"""
    name: str = "pytest_unit_test_generator"
    description: str = "分析源代码并自动生成pytest单元测试用例"
    args_schema: Type[BaseModel] = UnitTestGenerationInput
    
    def _run(
        self, 
        source_file: str,
        target_class: Optional[str] = None,
        test_type: str = "unit",
        include_mocks: bool = True,
        test_coverage: str = "basic"
    ) -> str:
        """生成单元测试代码"""
        try:
            # 读取源代码文件
            source_code = self._read_source_file(source_file)
            if not source_code:
                return f"❌ 无法读取源文件: {source_file}"
            
            # 分析代码结构
            code_analysis = self._analyze_code_structure(source_code, source_file)
            
            # 生成测试代码
            test_code = self._generate_test_code(
                code_analysis, target_class, test_type, include_mocks, test_coverage
            )
            
            # 保存测试文件
            test_file_path = self._get_test_file_path(source_file, test_type)
            self._save_test_file(test_file_path, test_code)
            
            return f"✅ 成功生成{test_type}测试文件: {test_file_path}\n\n预览:\n{test_code[:500]}..."
            
        except Exception as e:
            return f"❌ 测试生成失败: {str(e)}"
    
    def _read_source_file(self, file_path: str) -> str:
        """读取源代码文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return ""
    
    def _analyze_code_structure(self, source_code: str, file_path: str) -> Dict[str, Any]:
        """分析代码结构"""
        analysis = {
            'classes': [],
            'functions': [],
            'imports': [],
            'file_path': file_path
        }
        
        try:
            tree = ast.parse(source_code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = []
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            methods.append({
                                'name': item.name,
                                'args': [arg.arg for arg in item.args.args],
                                'is_async': isinstance(item, ast.AsyncFunctionDef)
                            })
                    
                    analysis['classes'].append({
                        'name': node.name,
                        'methods': methods
                    })
                
                elif isinstance(node, ast.FunctionDef):
                    if not any(node.name in cls['methods'] for cls in analysis['classes']):
                        analysis['functions'].append({
                            'name': node.name,
                            'args': [arg.arg for arg in node.args.args],
                            'is_async': isinstance(node, ast.AsyncFunctionDef)
                        })
                
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis['imports'].append(alias.name)
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for alias in node.names:
                            analysis['imports'].append(f"{node.module}.{alias.name}")
        
        except Exception as e:
            print(f"代码分析失败: {e}")
        
        return analysis
    
    def _generate_test_code(
        self, 
        analysis: Dict[str, Any],
        target_class: Optional[str],
        test_type: str,
        include_mocks: bool,
        test_coverage: str
    ) -> str:
        """生成测试代码"""
        
        # 基础导入
        imports = ['import pytest', 'from unittest.mock import Mock, patch, MagicMock']
        
        if include_mocks:
            imports.extend(['import asyncio', 'from datetime import datetime'])
        
        # 添加源文件导入
        source_imports = self._generate_source_imports(analysis['file_path'], analysis)
        imports.extend(source_imports)
        
        test_code = f'''"""
{os.path.basename(analysis['file_path'])} 的{test_type}测试
自动生成的测试用例 - 请根据实际业务逻辑调整
"""

{chr(10).join(imports)}


'''
        
        # 生成测试类
        if analysis['classes']:
            for cls_info in analysis['classes']:
                if target_class is None or cls_info['name'] == target_class:
                    test_code += self._generate_class_tests(cls_info, test_type, include_mocks, test_coverage)
        
        # 生成函数测试
        if analysis['functions']:
            test_code += self._generate_function_tests(analysis['functions'], test_type, include_mocks)
        
        return test_code
    
    def _generate_source_imports(self, file_path: str, analysis: Dict[str, Any]) -> List[str]:
        """生成源文件导入语句"""
        imports = []
        
        # 从文件路径生成导入路径
        if 'backend' in file_path:
            # 处理backend路径
            parts = file_path.replace('/Users/chiyingjie/code/git/claude-fastapi/', '').replace('.py', '').split('/')
            if 'backend' in parts:
                backend_index = parts.index('backend')
                import_path = '.'.join(parts[backend_index:])
                
                # 导入类和函数
                for cls_info in analysis['classes']:
                    imports.append(f"from {import_path} import {cls_info['name']}")
                
                for func_info in analysis['functions']:
                    imports.append(f"from {import_path} import {func_info['name']}")
        
        return imports
    
    def _generate_class_tests(self, cls_info: Dict[str, Any], test_type: str, include_mocks: bool, test_coverage: str) -> str:
        """生成类测试代码"""
        class_name = cls_info['name']
        test_class_name = f"Test{class_name}"
        
        test_code = f'''
class {test_class_name}:
    """{class_name}类测试"""
    
    @pytest.fixture
    def {class_name.lower()}_instance(self):
        """创建{class_name}实例"""
        return {class_name}()
    
'''
        
        if include_mocks:
            test_code += f'''    @pytest.fixture
    def mock_db_session(self):
        """Mock数据库会话"""
        mock_session = Mock()
        mock_session.commit.return_value = None
        mock_session.rollback.return_value = None
        return mock_session
    
'''
        
        # 为每个方法生成测试
        for method in cls_info['methods']:
            if not method['name'].startswith('_'):  # 跳过私有方法
                test_code += self._generate_method_test(method, class_name, test_type, include_mocks)
        
        return test_code
    
    def _generate_method_test(self, method: Dict[str, Any], class_name: str, test_type: str, include_mocks: bool) -> str:
        """生成方法测试代码"""
        method_name = method['name']
        args = method['args']
        is_async = method['is_async']
        
        # 确定测试函数名
        test_func_name = f"test_{method_name}"
        if test_type == "integration":
            test_func_name = f"test_{method_name}_integration"
        
        # 构建参数列表
        fixture_args = [f"{class_name.lower()}_instance"]
        if include_mocks and len(args) > 1:  # 排除self参数
            fixture_args.append("mock_db_session")
        
        fixture_str = ", ".join(fixture_args)
        
        # 异步标记
        async_marker = "@pytest.mark.asyncio\n    " if is_async else ""
        async_keyword = "async " if is_async else ""
        await_keyword = "await " if is_async else ""
        
        test_code = f'''    @pytest.mark.{test_type}
    {async_marker}def {test_func_name}(self, {fixture_str}):
        """测试{method_name}方法"""
        # 准备测试数据
        # TODO: 根据实际业务逻辑设置测试数据
        
        # 执行测试
        {await_keyword}result = {await_keyword}{class_name.lower()}_instance.{method_name}()
        
        # 验证结果
        # TODO: 根据预期结果进行断言
        assert result is not None
        
        # 验证Mock调用 (如果使用Mock)
        # mock_db_session.commit.assert_called_once()
    
'''
        
        return test_code
    
    def _generate_function_tests(self, functions: List[Dict[str, Any]], test_type: str, include_mocks: bool) -> str:
        """生成独立函数测试"""
        test_code = '''
class TestUtilityFunctions:
    """工具函数测试类"""
    
'''
        
        for func in functions:
            if not func['name'].startswith('_'):  # 跳过私有函数
                func_name = func['name']
                is_async = func['is_async']
                
                async_marker = "@pytest.mark.asyncio\n    " if is_async else ""
                async_keyword = "async " if is_async else ""
                await_keyword = "await " if is_async else ""
                
                test_code += f'''    @pytest.mark.{test_type}
    {async_marker}def test_{func_name}(self):
        """测试{func_name}函数"""
        # 准备测试数据
        # TODO: 设置函数参数
        
        # 执行测试
        result = {await_keyword}{func_name}()
        
        # 验证结果
        # TODO: 验证函数返回值
        assert result is not None
    
'''
        
        return test_code
    
    def _get_test_file_path(self, source_file: str, test_type: str) -> str:
        """获取测试文件路径"""
        # 确定测试目录
        if 'backend' in source_file:
            backend_path = source_file.split('backend')[0] + 'backend'
            relative_path = source_file.replace(backend_path + '/', '')
            
            # 构建测试文件路径
            test_dir = f"{backend_path}/tests/{test_type}"
            os.makedirs(test_dir, exist_ok=True)
            
            # 生成测试文件名
            filename = os.path.basename(source_file).replace('.py', '')
            test_filename = f"test_{filename}.py"
            
            return os.path.join(test_dir, test_filename)
        
        # 默认路径
        return f"test_{os.path.basename(source_file)}"
    
    def _save_test_file(self, file_path: str, test_code: str):
        """保存测试文件"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(test_code)


class APITestGenerationInput(BaseModel):
    """API测试生成输入"""
    api_file: str = Field(..., description="API路由文件路径")
    base_url: str = Field(default="http://localhost:8000", description="API基础URL")
    include_auth: bool = Field(default=True, description="是否包含认证测试")


class APITestGenerationTool(BaseTool):
    """API接口测试生成工具"""
    name: str = "api_test_generator"
    description: str = "分析FastAPI路由并生成API测试用例"
    args_schema: Type[BaseModel] = APITestGenerationInput
    
    def _run(self, api_file: str, base_url: str = "http://localhost:8000", include_auth: bool = True) -> str:
        """生成API测试代码"""
        try:
            # 读取API文件
            api_code = self._read_source_file(api_file)
            if not api_code:
                return f"❌ 无法读取API文件: {api_file}"
            
            # 分析API端点
            endpoints = self._analyze_api_endpoints(api_code)
            
            # 生成测试代码
            test_code = self._generate_api_test_code(endpoints, base_url, include_auth)
            
            # 保存测试文件
            test_file_path = self._get_api_test_file_path(api_file)
            self._save_test_file(test_file_path, test_code)
            
            return f"✅ 成功生成API测试文件: {test_file_path}\n\n预览:\n{test_code[:500]}..."
            
        except Exception as e:
            return f"❌ API测试生成失败: {str(e)}"
    
    def _read_source_file(self, file_path: str) -> str:
        """读取源代码文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return ""
    
    def _analyze_api_endpoints(self, api_code: str) -> List[Dict[str, Any]]:
        """分析API端点"""
        endpoints = []
        
        # 正则表达式匹配路由装饰器
        route_pattern = r'@router\.(get|post|put|delete|patch)\(\s*["\']([^"\']+)["\']'
        matches = re.findall(route_pattern, api_code)
        
        for method, path in matches:
            endpoints.append({
                'method': method.upper(),
                'path': path,
                'function_name': self._extract_function_name(api_code, method, path)
            })
        
        return endpoints
    
    def _extract_function_name(self, api_code: str, method: str, path: str) -> str:
        """提取端点对应的函数名"""
        # 简单的函数名提取逻辑
        lines = api_code.split('\n')
        for i, line in enumerate(lines):
            if f'@router.{method}(' in line and f'"{path}"' in line:
                # 查找下一个函数定义
                for j in range(i+1, min(i+10, len(lines))):
                    if lines[j].strip().startswith('def ') or lines[j].strip().startswith('async def '):
                        func_line = lines[j].strip()
                        func_name = func_line.split('(')[0].replace('async def ', '').replace('def ', '')
                        return func_name
        
        return f"{method.lower()}_{path.replace('/', '_').replace('{', '').replace('}', '')}"
    
    def _generate_api_test_code(self, endpoints: List[Dict[str, Any]], base_url: str, include_auth: bool) -> str:
        """生成API测试代码"""
        
        test_code = f'''"""
API接口测试
自动生成的API测试用例 - 请根据实际API规范调整
"""

import pytest
import httpx
from fastapi.testclient import TestClient
from datetime import datetime

# 如果需要导入应用实例
# from backend.main import app
# client = TestClient(app)

BASE_URL = "{base_url}"


@pytest.fixture
def client():
    """HTTP客户端fixture"""
    return httpx.Client(base_url=BASE_URL)


@pytest.fixture
def auth_headers():
    """认证头部fixture"""
    # TODO: 实现实际的认证逻辑
    return {{"Authorization": "Bearer test_token"}}


class TestAPIEndpoints:
    """API端点测试类"""
    
'''

        # 为每个端点生成测试方法
        for endpoint in endpoints:
            test_code += self._generate_endpoint_test(endpoint, include_auth)
        
        return test_code
    
    def _generate_endpoint_test(self, endpoint: Dict[str, Any], include_auth: bool) -> str:
        """生成单个端点的测试方法"""
        method = endpoint['method']
        path = endpoint['path']
        func_name = endpoint['function_name']
        
        # 生成测试数据
        test_data = self._generate_test_data_for_method(method)
        
        # 认证参数
        auth_param = ", auth_headers" if include_auth else ""
        auth_usage = "headers=auth_headers" if include_auth else ""
        
        test_code = f'''
    @pytest.mark.api
    def test_{func_name}(self, client{auth_param}):
        """测试 {method} {path}"""
        # 准备测试数据
        {test_data}
        
        # 发送请求
        response = client.{method.lower()}(
            "{path}",
            {auth_usage}{',' if auth_usage and test_data.strip() else ''}
            {test_data.strip()}
        )
        
        # 验证响应
        assert response.status_code in [200, 201, 204]
        
        # 验证响应格式
        if response.status_code != 204:  # 非空响应
            response_data = response.json()
            assert response_data is not None
            
        # TODO: 添加业务逻辑验证
        
'''
        
        return test_code
    
    def _generate_test_data_for_method(self, method: str) -> str:
        """根据HTTP方法生成测试数据"""
        if method in ['POST', 'PUT', 'PATCH']:
            return '''test_data = {
            "name": "测试数据",
            "description": "自动生成的测试数据"
        }
        json=test_data,'''
        elif method == 'GET':
            return '''params={"page": 1, "limit": 10},'''
        else:
            return ''
    
    def _get_api_test_file_path(self, api_file: str) -> str:
        """获取API测试文件路径"""
        if 'backend' in api_file:
            backend_path = api_file.split('backend')[0] + 'backend'
            test_dir = f"{backend_path}/tests/api"
            os.makedirs(test_dir, exist_ok=True)
            
            filename = os.path.basename(api_file).replace('.py', '')
            test_filename = f"test_{filename}.py"
            
            return os.path.join(test_dir, test_filename)
        
        return f"test_api_{os.path.basename(api_file)}"
    
    def _save_test_file(self, file_path: str, test_code: str):
        """保存测试文件"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(test_code)


class MockDataGenerationInput(BaseModel):
    """Mock数据生成输入"""
    model_name: str = Field(..., description="数据模型名称")
    data_type: str = Field(default="factory", description="数据类型: factory, fixture, sample")
    quantity: int = Field(default=10, description="生成数据数量")


class MockDataGenerationTool(BaseTool):
    """测试数据和Mock生成工具"""
    name: str = "mock_data_generator"
    description: str = "生成测试用的Mock数据和Factory类"
    args_schema: Type[BaseModel] = MockDataGenerationInput
    
    def _run(self, model_name: str, data_type: str = "factory", quantity: int = 10) -> str:
        """生成Mock数据"""
        try:
            if data_type == "factory":
                mock_code = self._generate_factory_class(model_name)
            elif data_type == "fixture":
                mock_code = self._generate_pytest_fixtures(model_name, quantity)
            else:
                mock_code = self._generate_sample_data(model_name, quantity)
            
            # 保存Mock文件
            mock_file_path = self._get_mock_file_path(model_name, data_type)
            self._save_mock_file(mock_file_path, mock_code)
            
            return f"✅ 成功生成{data_type}数据文件: {mock_file_path}\n\n预览:\n{mock_code[:300]}..."
            
        except Exception as e:
            return f"❌ Mock数据生成失败: {str(e)}"
    
    def _generate_factory_class(self, model_name: str) -> str:
        """生成Factory类"""
        return f'''"""
{model_name} Factory类
用于生成测试用的{model_name}对象
"""

import factory
from factory import fuzzy
from datetime import datetime

from backend.models.{model_name.lower()} import {model_name}


class {model_name}Factory(factory.Factory):
    """
    {model_name}对象工厂类
    使用 factory_boy 生成测试数据
    """
    
    class Meta:
        model = {model_name}
    
    # 基础字段 (需要根据实际模型调整)
    id = factory.Sequence(lambda n: n)
    name = factory.Faker('name', locale='zh_CN')
    email = factory.Faker('email')
    description = factory.Faker('text', max_nb_chars=200, locale='zh_CN')
    
    # 时间字段
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)
    
    # 状态字段
    is_active = factory.Faker('boolean', chance_of_getting_true=80)
    
    @factory.post_generation
    def set_password(obj, create, extracted, **kwargs):
        """设置密码 (如果有密码字段)"""
        if hasattr(obj, 'password'):
            obj.password = "test_password_123"


# 便捷创建函数
def create_{model_name.lower()}(**kwargs):
    """创建{model_name}对象"""
    return {model_name}Factory(**kwargs)


def create_{model_name.lower()}_batch(size=10, **kwargs):
    """批量创建{model_name}对象"""
    return {model_name}Factory.create_batch(size, **kwargs)
'''
    
    def _generate_pytest_fixtures(self, model_name: str, quantity: int) -> str:
        """生成pytest fixtures"""
        return f'''"""
{model_name} pytest fixtures
提供测试用的{model_name}数据fixtures
"""

import pytest
from datetime import datetime
from unittest.mock import Mock

from backend.models.{model_name.lower()} import {model_name}


@pytest.fixture
def sample_{model_name.lower()}():
    """单个{model_name}对象fixture"""
    return {model_name}(
        id=1,
        name="测试{model_name}",
        description="这是一个测试用的{model_name}对象",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def {model_name.lower()}_list():
    """{model_name}对象列表fixture"""
    {model_name.lower()}s = []
    for i in range({quantity}):
        {model_name.lower()}_obj = {model_name}(
            id=i + 1,
            name=f"测试{model_name}{{i+1}}",
            description=f"这是第{{i+1}}个测试{model_name}",
            is_active=i % 2 == 0,  # 交替设置激活状态
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        {model_name.lower()}s.append({model_name.lower()}_obj)
    
    return {model_name.lower()}s


@pytest.fixture
def mock_{model_name.lower()}():
    """Mock {model_name}对象fixture"""
    mock_obj = Mock(spec={model_name})
    mock_obj.id = 1
    mock_obj.name = "Mock{model_name}"
    mock_obj.description = "这是一个Mock对象"
    mock_obj.is_active = True
    mock_obj.created_at = datetime.now()
    mock_obj.updated_at = datetime.now()
    
    return mock_obj


@pytest.fixture
def {model_name.lower()}_create_data():
    """创建{model_name}的测试数据"""
    return {{
        "name": "新{model_name}",
        "description": "通过API创建的{model_name}",
        "is_active": True
    }}


@pytest.fixture
def {model_name.lower()}_update_data():
    """更新{model_name}的测试数据"""
    return {{
        "name": "更新后的{model_name}",
        "description": "更新后的描述信息",
        "is_active": False
    }}
'''
    
    def _generate_sample_data(self, model_name: str, quantity: int) -> str:
        """生成示例数据"""
        return f'''"""
{model_name}示例数据
提供测试用的静态数据
"""

from datetime import datetime

# 单个示例对象
SAMPLE_{model_name.upper()} = {{
    "id": 1,
    "name": "示例{model_name}",
    "description": "这是一个示例{model_name}对象",
    "is_active": True,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
}}

# 示例对象列表
SAMPLE_{model_name.upper()}_LIST = [
    {{
        "id": i + 1,
        "name": f"示例{model_name}{{i+1}}",
        "description": f"这是第{{i+1}}个示例{model_name}",
        "is_active": i % 2 == 0,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }}
    for i in range({quantity})
]

# API测试数据
{model_name.upper()}_CREATE_PAYLOAD = {{
    "name": "API创建的{model_name}",
    "description": "通过API创建的{model_name}对象",
    "is_active": True
}}

{model_name.upper()}_UPDATE_PAYLOAD = {{
    "name": "API更新的{model_name}",
    "description": "通过API更新的{model_name}对象",
    "is_active": False
}}

# 无效数据示例 (用于测试验证)
INVALID_{model_name.upper()}_DATA = [
    {{}},  # 空数据
    {{"name": ""}},  # 空名称
    {{"name": "a" * 256}},  # 名称过长
    {{"email": "invalid_email"}},  # 无效邮箱格式
]
'''
    
    def _get_mock_file_path(self, model_name: str, data_type: str) -> str:
        """获取Mock文件路径"""
        backend_path = "/Users/chiyingjie/code/git/claude-fastapi/backend"
        test_dir = f"{backend_path}/tests/fixtures"
        os.makedirs(test_dir, exist_ok=True)
        
        if data_type == "factory":
            filename = f"{model_name.lower()}_factory.py"
        elif data_type == "fixture":
            filename = f"{model_name.lower()}_fixtures.py"
        else:
            filename = f"{model_name.lower()}_data.py"
        
        return os.path.join(test_dir, filename)
    
    def _save_mock_file(self, file_path: str, mock_code: str):
        """保存Mock文件"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(mock_code)


class PerformanceTestGenerationInput(BaseModel):
    """性能测试生成输入"""
    target_endpoint: str = Field(..., description="目标API端点")
    test_type: str = Field(default="load", description="测试类型: load, stress, spike")
    user_count: int = Field(default=100, description="并发用户数")
    duration: str = Field(default="5m", description="测试持续时间")


class PerformanceTestGenerationTool(BaseTool):
    """性能测试生成工具"""
    name: str = "performance_test_generator"
    description: str = "生成Locust性能测试脚本"
    args_schema: Type[BaseModel] = PerformanceTestGenerationInput
    
    def _run(
        self,
        target_endpoint: str,
        test_type: str = "load",
        user_count: int = 100,
        duration: str = "5m"
    ) -> str:
        """生成性能测试脚本"""
        try:
            test_script = self._generate_locust_script(target_endpoint, test_type, user_count, duration)
            
            # 保存测试脚本
            script_path = self._get_performance_test_path(target_endpoint, test_type)
            self._save_test_script(script_path, test_script)
            
            return f"✅ 成功生成{test_type}性能测试脚本: {script_path}\n\n预览:\n{test_script[:400]}..."
            
        except Exception as e:
            return f"❌ 性能测试生成失败: {str(e)}"
    
    def _generate_locust_script(self, endpoint: str, test_type: str, user_count: int, duration: str) -> str:
        """生成Locust测试脚本"""
        return f'''"""
{endpoint} 性能测试脚本
测试类型: {test_type}
并发用户: {user_count}
持续时间: {duration}
"""

from locust import HttpUser, task, between
import random
import json


class {test_type.title()}TestUser(HttpUser):
    """
    {test_type}测试用户类
    模拟用户行为进行性能测试
    """
    
    # 用户等待时间 (秒)
    wait_time = between(1, 3)
    
    def on_start(self):
        """测试开始时执行"""
        # 登录获取token (如果需要认证)
        self.login()
    
    def login(self):
        """用户登录"""
        login_data = {{
            "username": f"testuser{{random.randint(1, 1000)}}",
            "password": "test_password"
        }}
        
        response = self.client.post("/api/v1/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            self.client.headers.update({{"Authorization": f"Bearer {{token}}"}})
    
    @task(3)
    def test_target_endpoint(self):
        """测试目标端点: {endpoint}"""
        response = self.client.get("{endpoint}")
        
        # 验证响应
        if response.status_code != 200:
            print(f"请求失败: {{response.status_code}} - {{response.text}}")
    
    @task(2)
    def test_list_endpoint(self):
        """测试列表端点"""
        params = {{
            "page": random.randint(1, 10),
            "limit": random.choice([10, 20, 50])
        }}
        
        response = self.client.get("{endpoint.rsplit('/', 1)[0]}", params=params)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                # 随机访问详情页
                item_id = data[0].get("id")
                if item_id:
                    self.client.get(f"{endpoint.rsplit('/', 1)[0]}/{{item_id}}")
    
    @task(1)
    def test_create_operation(self):
        """测试创建操作"""
        create_data = {{
            "name": f"性能测试数据{{random.randint(1, 10000)}}",
            "description": f"Locust性能测试创建的数据 - {{random.randint(1, 10000)}}",
            "is_active": random.choice([True, False])
        }}
        
        response = self.client.post("{endpoint.rsplit('/', 1)[0]}", json=create_data)
        
        if response.status_code in [200, 201]:
            # 创建成功后尝试获取
            created_item = response.json()
            if "id" in created_item:
                self.client.get(f"{endpoint.rsplit('/', 1)[0]}/{{created_item['id']}}")


# 测试配置
if __name__ == "__main__":
    import os
    
    # 设置测试参数
    os.environ["LOCUST_USERS"] = "{user_count}"
    os.environ["LOCUST_SPAWN_RATE"] = "10"
    os.environ["LOCUST_RUN_TIME"] = "{duration}"
    os.environ["LOCUST_HOST"] = "http://localhost:8000"
    
    print("开始{test_type}测试:")
    print(f"目标端点: {endpoint}")
    print(f"并发用户: {user_count}")
    print(f"测试时长: {duration}")
    print("运行命令: locust -f {os.path.basename(__file__)}")
'''
    
    def _get_performance_test_path(self, endpoint: str, test_type: str) -> str:
        """获取性能测试脚本路径"""
        backend_path = "/Users/chiyingjie/code/git/claude-fastapi/backend"
        test_dir = f"{backend_path}/tests/performance"
        os.makedirs(test_dir, exist_ok=True)
        
        # 从端点生成文件名
        endpoint_name = endpoint.replace('/', '_').replace('{', '').replace('}', '').strip('_')
        filename = f"{test_type}_{endpoint_name}_test.py"
        
        return os.path.join(test_dir, filename)
    
    def _save_test_script(self, file_path: str, script_content: str):
        """保存测试脚本"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(script_content)


# 导出所有工具
__all__ = [
    "UnitTestGenerationTool",
    "APITestGenerationTool",
    "MockDataGenerationTool",
    "PerformanceTestGenerationTool"
]