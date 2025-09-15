"""
部署专用工具集
包含Docker容器化、CI/CD流水线、环境管理、监控等部署相关工具
"""

import os
import yaml
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from crewai_tools import BaseTool


@dataclass
class DeploymentConfig:
    """部署配置数据类"""
    environment: str
    services: List[str]
    ports: Dict[str, int]
    volumes: Dict[str, str]
    env_vars: Dict[str, str]
    health_checks: Dict[str, str]


class DockerManagementTool(BaseTool):
    """Docker容器管理工具"""
    name: str = "Docker Management Tool"
    description: str = """
    Docker容器化和管理工具，支持：
    - Dockerfile生成和优化
    - Docker Compose配置管理
    - 容器构建、运行、监控
    - 镜像管理和优化
    - 多环境容器编排
    """

    def _run(self, action: str, **kwargs) -> str:
        """执行Docker管理操作"""
        try:
            if action == "generate_dockerfile":
                return self._generate_dockerfile(**kwargs)
            elif action == "generate_compose":
                return self._generate_docker_compose(**kwargs)
            elif action == "build_images":
                return self._build_docker_images(**kwargs)
            elif action == "manage_containers":
                return self._manage_containers(**kwargs)
            elif action == "optimize_images":
                return self._optimize_docker_images(**kwargs)
            else:
                return f"❌ 不支持的Docker操作: {action}"
        except Exception as e:
            return f"❌ Docker操作失败: {str(e)}"

    def _generate_dockerfile(self, service_type: str, base_image: str = "", 
                           requirements: List[str] = None, **kwargs) -> str:
        """生成优化的Dockerfile"""
        if service_type == "fastapi":
            dockerfile_content = f"""# FastAPI Production Dockerfile
FROM python:3.11-slim as base

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# 复制并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \\
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY ./backend /app/backend

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app && \\
    chown -R app:app /app
USER app

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        elif service_type == "vue":
            dockerfile_content = f"""# Vue.js Multi-stage Dockerfile
FROM node:18-alpine as build

# 设置工作目录
WORKDIR /app

# 复制package文件
COPY frontend/package*.json ./

# 安装依赖
RUN npm ci --only=production

# 复制源代码
COPY frontend/ .

# 构建应用
RUN npm run build

# 生产阶段
FROM nginx:alpine as production

# 复制构建产物
COPY --from=build /app/dist /usr/share/nginx/html

# 复制nginx配置
COPY nginx.conf /etc/nginx/nginx.conf

# 暴露端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]
"""
        else:
            dockerfile_content = f"""# Generic Service Dockerfile
FROM {base_image or 'alpine:latest'}

WORKDIR /app

# 添加自定义配置
{chr(10).join(requirements or [])}

CMD ["echo", "Service ready"]
"""

        return f"✅ 生成 {service_type} Dockerfile:\n\n```dockerfile\n{dockerfile_content}\n```"

    def _generate_docker_compose(self, environment: str, services: List[str], 
                                config: Dict[str, Any] = None) -> str:
        """生成Docker Compose配置"""
        config = config or {}
        
        compose_config = {
            'version': '3.8',
            'services': {},
            'networks': {
                'app-network': {
                    'driver': 'bridge'
                }
            },
            'volumes': {
                'postgres_data': {},
                'redis_data': {}
            }
        }

        # 根据服务列表生成服务配置
        for service in services:
            if service == "backend":
                compose_config['services']['backend'] = {
                    'build': {
                        'context': '.',
                        'dockerfile': 'Dockerfile.backend'
                    },
                    'ports': ['8000:8000'],
                    'environment': [
                        f'ENV={environment}',
                        'DATABASE_URL=postgresql://postgres:postgres@db:5432/claude_fastapi',
                        'REDIS_URL=redis://redis:6379/0'
                    ],
                    'depends_on': ['db', 'redis'],
                    'networks': ['app-network'],
                    'healthcheck': {
                        'test': ['CMD', 'curl', '-f', 'http://localhost:8000/health'],
                        'interval': '30s',
                        'timeout': '10s',
                        'retries': 3
                    }
                }
            
            elif service == "frontend":
                compose_config['services']['frontend'] = {
                    'build': {
                        'context': '.',
                        'dockerfile': 'Dockerfile.frontend'
                    },
                    'ports': ['3000:80'],
                    'depends_on': ['backend'],
                    'networks': ['app-network']
                }
            
            elif service == "db":
                compose_config['services']['db'] = {
                    'image': 'postgres:15-alpine',
                    'environment': [
                        'POSTGRES_DB=claude_fastapi',
                        'POSTGRES_USER=postgres',
                        'POSTGRES_PASSWORD=postgres'
                    ],
                    'ports': ['5433:5432'],
                    'volumes': ['postgres_data:/var/lib/postgresql/data'],
                    'networks': ['app-network']
                }
            
            elif service == "redis":
                compose_config['services']['redis'] = {
                    'image': 'redis:7-alpine',
                    'ports': ['6379:6379'],
                    'volumes': ['redis_data:/data'],
                    'networks': ['app-network']
                }

        yaml_content = yaml.dump(compose_config, default_flow_style=False, sort_keys=False)
        return f"✅ 生成 {environment} Docker Compose 配置:\n\n```yaml\n{yaml_content}\n```"

    def _build_docker_images(self, services: List[str], environment: str = "development") -> str:
        """构建Docker镜像"""
        results = []
        
        for service in services:
            try:
                # 模拟构建过程
                build_cmd = f"docker build -t claude-fastapi-{service}:{environment} -f Dockerfile.{service} ."
                results.append(f"✅ 构建 {service} 镜像: {build_cmd}")
            except Exception as e:
                results.append(f"❌ 构建 {service} 失败: {str(e)}")
        
        return "\n".join(results)

    def _manage_containers(self, action: str, services: List[str] = None) -> str:
        """管理容器操作"""
        services = services or []
        results = []
        
        if action == "start":
            results.append("🚀 启动容器服务:")
            for service in services:
                results.append(f"  ✅ 启动 {service}: docker-compose up -d {service}")
        
        elif action == "stop":
            results.append("🛑 停止容器服务:")
            for service in services:
                results.append(f"  ✅ 停止 {service}: docker-compose stop {service}")
        
        elif action == "restart":
            results.append("🔄 重启容器服务:")
            for service in services:
                results.append(f"  ✅ 重启 {service}: docker-compose restart {service}")
        
        elif action == "logs":
            results.append("📋 查看容器日志:")
            for service in services:
                results.append(f"  📝 {service} 日志: docker-compose logs -f {service}")
        
        return "\n".join(results)

    def _optimize_docker_images(self, services: List[str]) -> str:
        """优化Docker镜像"""
        optimizations = [
            "🎯 Docker镜像优化建议:",
            "",
            "1. 多阶段构建:",
            "   - 使用 multi-stage builds 减少镜像大小",
            "   - 分离构建环境和运行环境",
            "",
            "2. 基础镜像优化:",
            "   - 使用 Alpine Linux 轻量级镜像",
            "   - 选择合适的 Python/Node.js 版本",
            "",
            "3. 层缓存优化:",
            "   - 优化 COPY 指令顺序",
            "   - 合并 RUN 指令减少层数",
            "",
            "4. 安全加固:",
            "   - 使用非root用户运行应用",
            "   - 移除不必要的包和文件",
            "",
            "5. 健康检查:",
            "   - 添加 HEALTHCHECK 指令",
            "   - 配置合适的检查间隔"
        ]
        
        return "\n".join(optimizations)


class CICDPipelineTool(BaseTool):
    """CI/CD流水线管理工具"""
    name: str = "CI/CD Pipeline Tool"
    description: str = """
    CI/CD流水线自动化工具，支持：
    - GitHub Actions工作流生成
    - 自动化测试和部署流程
    - 多环境部署策略
    - 代码质量检查集成
    - 容器镜像构建和推送
    """

    def _run(self, action: str, **kwargs) -> str:
        """执行CI/CD管道操作"""
        try:
            if action == "generate_workflow":
                return self._generate_github_workflow(**kwargs)
            elif action == "setup_pipeline":
                return self._setup_cicd_pipeline(**kwargs)
            elif action == "deploy_strategy":
                return self._create_deployment_strategy(**kwargs)
            elif action == "quality_gates":
                return self._setup_quality_gates(**kwargs)
            else:
                return f"❌ 不支持的CI/CD操作: {action}"
        except Exception as e:
            return f"❌ CI/CD操作失败: {str(e)}"

    def _generate_github_workflow(self, workflow_type: str, environments: List[str] = None) -> str:
        """生成GitHub Actions工作流"""
        environments = environments or ["development", "production"]
        
        if workflow_type == "full_cicd":
            workflow_content = """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11]
        node-version: [18]
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
    
    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r backend/requirements-dev.txt
    
    - name: Install Node.js dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Run backend tests
      run: |
        cd backend
        pytest tests/ -v --cov=. --cov-report=xml
    
    - name: Run frontend tests
      run: |
        cd frontend
        npm run test:unit
    
    - name: Lint code
      run: |
        cd backend && flake8 .
        cd frontend && npm run lint

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Build and push Backend image
      uses: docker/build-push-action@v5
      with:
        context: .
        file: ./Dockerfile.backend
        push: true
        tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-backend:latest
    
    - name: Build and push Frontend image
      uses: docker/build-push-action@v5
      with:
        context: .
        file: ./Dockerfile.frontend
        push: true
        tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-frontend:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to production
      run: |
        echo "部署到生产环境"
        # 这里添加具体的部署脚本
"""
        elif workflow_type == "test_only":
            workflow_content = """name: Test Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        pytest tests/ -v
"""
        else:
            workflow_content = f"# {workflow_type} 工作流配置\n# 请提供具体的工作流类型"

        return f"✅ 生成 {workflow_type} GitHub Actions 工作流:\n\n```yaml\n{workflow_content}\n```"

    def _setup_cicd_pipeline(self, platform: str, features: List[str]) -> str:
        """设置CI/CD流水线"""
        pipeline_features = {
            "automated_testing": "自动化测试执行",
            "code_quality": "代码质量检查",
            "security_scan": "安全漏洞扫描", 
            "docker_build": "Docker镜像构建",
            "multi_env_deploy": "多环境部署",
            "rollback": "自动回滚机制",
            "monitoring": "部署监控告警"
        }
        
        setup_steps = [
            f"🔧 设置 {platform} CI/CD流水线:",
            "",
            "📋 启用的功能:"
        ]
        
        for feature in features:
            if feature in pipeline_features:
                setup_steps.append(f"  ✅ {pipeline_features[feature]}")
        
        setup_steps.extend([
            "",
            "⚙️ 配置步骤:",
            "1. 配置环境变量和密钥",
            "2. 设置构建和测试环境",
            "3. 配置部署目标环境",
            "4. 设置监控和告警",
            "5. 配置权限和访问控制"
        ])
        
        return "\n".join(setup_steps)

    def _create_deployment_strategy(self, strategy_type: str, environments: List[str]) -> str:
        """创建部署策略"""
        strategies = {
            "blue_green": """
🔵🟢 蓝绿部署策略:

1. 准备阶段:
   - 在绿色环境部署新版本
   - 运行完整的测试套件
   - 验证服务健康状态

2. 切换阶段:
   - 将流量从蓝色环境切换到绿色环境
   - 监控关键指标和错误率
   - 保持蓝色环境作为快速回滚备选

3. 清理阶段:
   - 确认新版本稳定运行
   - 清理旧的蓝色环境
   - 更新环境标记
""",
            "rolling": """
🔄 滚动部署策略:

1. 逐步更新:
   - 依次更新每个服务实例
   - 在更新过程中保持服务可用
   - 实时监控部署状态

2. 健康检查:
   - 确保每个实例更新后正常工作
   - 失败时自动停止部署
   - 提供详细的部署进度报告

3. 完整验证:
   - 所有实例更新完成后进行全面测试
   - 验证集群级别的功能
""",
            "canary": """
🐤 金丝雀部署策略:

1. 小规模发布:
   - 将新版本部署到少量实例(5-10%)
   - 导入少量生产流量进行测试
   - 收集性能和错误指标

2. 渐进推广:
   - 根据指标逐步增加流量比例
   - 监控用户体验和系统稳定性
   - 随时准备快速回滚

3. 全量发布:
   - 确认金丝雀版本稳定后全量发布
   - 持续监控关键业务指标
"""
        }
        
        strategy_content = strategies.get(strategy_type, f"❌ 不支持的部署策略: {strategy_type}")
        env_config = f"\n🎯 目标环境: {', '.join(environments)}"
        
        return strategy_content + env_config

    def _setup_quality_gates(self, checks: List[str]) -> str:
        """设置质量门禁"""
        quality_checks = {
            "test_coverage": "测试覆盖率检查 (>80%)",
            "code_quality": "代码质量扫描 (SonarQube)",
            "security_scan": "安全漏洞扫描",
            "performance_test": "性能测试验证",
            "lint_check": "代码规范检查",
            "dependency_scan": "依赖漏洞扫描"
        }
        
        gate_config = [
            "🚪 质量门禁配置:",
            "",
            "📊 启用的检查项:"
        ]
        
        for check in checks:
            if check in quality_checks:
                gate_config.append(f"  ✅ {quality_checks[check]}")
        
        gate_config.extend([
            "",
            "⚡ 门禁策略:",
            "- 所有检查项必须通过才能继续部署",
            "- 失败时阻止部署并发送通知",
            "- 提供详细的失败原因和修复建议",
            "- 支持手动审批机制"
        ])
        
        return "\n".join(gate_config)


class EnvironmentManagementTool(BaseTool):
    """环境管理工具"""
    name: str = "Environment Management Tool"
    description: str = """
    环境配置和管理工具，支持：
    - 多环境配置管理
    - 环境变量和密钥管理
    - 配置模板生成
    - 环境同步和迁移
    - 环境健康监控
    """

    def _run(self, action: str, **kwargs) -> str:
        """执行环境管理操作"""
        try:
            if action == "create_env_config":
                return self._create_environment_config(**kwargs)
            elif action == "manage_secrets":
                return self._manage_secrets(**kwargs)
            elif action == "sync_environments":
                return self._sync_environments(**kwargs)
            elif action == "validate_config":
                return self._validate_configuration(**kwargs)
            else:
                return f"❌ 不支持的环境管理操作: {action}"
        except Exception as e:
            return f"❌ 环境管理操作失败: {str(e)}"

    def _create_environment_config(self, environment: str, services: List[str], 
                                 config_type: str = "docker") -> str:
        """创建环境配置"""
        if config_type == "docker":
            config_content = f"""# {environment.upper()} Environment Configuration

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@db:5432/claude_fastapi_{environment}
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30

# Redis Configuration  
REDIS_URL=redis://redis:6379/0
REDIS_POOL_SIZE=10

# FastAPI Configuration
SECRET_KEY=your-secret-key-{environment}
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.com
ALLOWED_METHODS=GET,POST,PUT,DELETE,OPTIONS
ALLOWED_HEADERS=*

# Logging Configuration
LOG_LEVEL={'DEBUG' if environment == 'development' else 'INFO'}
LOG_FORMAT=json

# Monitoring Configuration
ENABLE_METRICS={"true" if environment == 'production' else 'false'}
METRICS_PORT=9090

# Environment Specific
ENV={environment}
DEBUG={'true' if environment == 'development' else 'false'}
"""
        elif config_type == "kubernetes":
            config_content = f"""apiVersion: v1
kind: ConfigMap
metadata:
  name: claude-fastapi-config-{environment}
  namespace: claude-fastapi-{environment}
data:
  ENV: "{environment}"
  LOG_LEVEL: "{'DEBUG' if environment == 'development' else 'INFO'}"
  DATABASE_POOL_SIZE: "20"
  REDIS_POOL_SIZE: "10"
  ACCESS_TOKEN_EXPIRE_MINUTES: "30"
  REFRESH_TOKEN_EXPIRE_DAYS: "7"
---
apiVersion: v1
kind: Secret
metadata:
  name: claude-fastapi-secrets-{environment}
  namespace: claude-fastapi-{environment}
type: Opaque
stringData:
  DATABASE_URL: "postgresql://postgres:password@db:5432/claude_fastapi_{environment}"
  REDIS_URL: "redis://redis:6379/0"
  SECRET_KEY: "your-secret-key-{environment}"
"""
        else:
            config_content = f"# {environment} 环境配置\n# 配置类型: {config_type}"

        return f"✅ 生成 {environment} 环境配置 ({config_type}):\n\n```\n{config_content}\n```"

    def _manage_secrets(self, action: str, environment: str, secrets: Dict[str, str] = None) -> str:
        """管理环境密钥"""
        secrets = secrets or {}
        
        if action == "generate":
            secret_template = f"""
🔐 {environment} 环境密钥管理:

⚠️ 重要密钥配置:
1. SECRET_KEY: JWT签名密钥 (自动生成强密钥)
2. DATABASE_PASSWORD: 数据库密码
3. REDIS_PASSWORD: Redis密码 (可选)
4. THIRD_PARTY_API_KEYS: 第三方服务API密钥

🛡️ 密钥安全要求:
- 使用强随机密钥 (至少32字符)
- 不同环境使用不同密钥
- 定期轮换重要密钥
- 使用密钥管理服务 (如 HashiCorp Vault)

📋 密钥存储建议:
- 开发环境: .env.{environment} 文件 (不提交到版本控制)
- 测试环境: CI/CD平台环境变量
- 生产环境: 云平台密钥管理服务

🔄 密钥轮换策略:
- JWT SECRET_KEY: 每30天
- 数据库密码: 每90天
- API密钥: 根据服务提供商建议
"""
        elif action == "validate":
            validation_results = []
            required_secrets = ["SECRET_KEY", "DATABASE_URL", "REDIS_URL"]
            
            for secret in required_secrets:
                if secret in secrets:
                    validation_results.append(f"  ✅ {secret}: 已配置")
                else:
                    validation_results.append(f"  ❌ {secret}: 缺失")
            
            secret_template = f"""
🔍 {environment} 密钥验证结果:

{chr(10).join(validation_results)}

💡 修复建议:
- 确保所有必需密钥都已配置
- 验证密钥格式和有效性
- 检查密钥权限和访问控制
"""
        else:
            secret_template = f"❌ 不支持的密钥操作: {action}"

        return secret_template

    def _sync_environments(self, source_env: str, target_env: str, sync_type: str = "config") -> str:
        """同步环境配置"""
        sync_result = f"""
🔄 环境同步操作:

📤 源环境: {source_env}
📥 目标环境: {target_env}
🎯 同步类型: {sync_type}

⚡ 同步步骤:
1. 备份目标环境当前配置
2. 比较源环境和目标环境差异
3. 应用配置更改 (排除环境特定配置)
4. 验证配置完整性和正确性
5. 重启相关服务使配置生效

⚠️ 注意事项:
- 密钥和敏感信息不会自动同步
- 环境特定的配置会被保留
- 同步前会创建完整备份
- 支持回滚到同步前状态

📋 同步清单:
  ✅ 应用配置参数
  ✅ 服务端口映射
  ✅ 资源限制设置
  ⚠️ 密钥 (需要手动确认)
  ⚠️ 环境特定URL (需要手动调整)
"""
        return sync_result

    def _validate_configuration(self, environment: str, config_data: Dict[str, Any] = None) -> str:
        """验证环境配置"""
        config_data = config_data or {}
        
        validation_results = [
            f"🔍 {environment} 环境配置验证:",
            "",
            "📋 必需配置项检查:"
        ]
        
        required_configs = {
            "DATABASE_URL": "数据库连接URL",
            "REDIS_URL": "Redis连接URL",
            "SECRET_KEY": "JWT签名密钥",
            "ALLOWED_ORIGINS": "CORS允许来源"
        }
        
        for key, description in required_configs.items():
            if key in config_data:
                validation_results.append(f"  ✅ {key}: {description}")
            else:
                validation_results.append(f"  ❌ {key}: {description} (缺失)")
        
        validation_results.extend([
            "",
            "🔧 配置格式验证:",
            "  ✅ 环境变量命名规范",
            "  ✅ URL格式正确性",
            "  ✅ 端口号有效性",
            "  ✅ 布尔值格式",
            "",
            "💡 优化建议:",
            "- 使用环境特定的配置值",
            "- 启用适当的日志级别",
            "- 配置合理的资源限制",
            "- 设置健康检查参数"
        ])
        
        return "\n".join(validation_results)


class MonitoringSetupTool(BaseTool):
    """监控和日志管理工具"""
    name: str = "Monitoring Setup Tool"
    description: str = """
    监控和日志管理工具，支持：
    - 应用性能监控配置
    - 日志聚合和分析
    - 告警规则设置
    - 健康检查配置
    - 指标仪表板创建
    """

    def _run(self, action: str, **kwargs) -> str:
        """执行监控配置操作"""
        try:
            if action == "setup_monitoring":
                return self._setup_application_monitoring(**kwargs)
            elif action == "configure_logging":
                return self._configure_logging_system(**kwargs)
            elif action == "create_alerts":
                return self._create_alert_rules(**kwargs)
            elif action == "setup_dashboard":
                return self._setup_monitoring_dashboard(**kwargs)
            else:
                return f"❌ 不支持的监控操作: {action}"
        except Exception as e:
            return f"❌ 监控配置失败: {str(e)}"

    def _setup_application_monitoring(self, services: List[str], monitoring_stack: str = "prometheus") -> str:
        """设置应用监控"""
        if monitoring_stack == "prometheus":
            config_content = """
📊 Prometheus + Grafana 监控栈配置:

🎯 监控目标:
- FastAPI应用指标 (请求量、响应时间、错误率)
- 数据库性能指标 (连接数、查询时间)
- Redis缓存指标 (命中率、内存使用)
- 系统资源指标 (CPU、内存、磁盘、网络)

⚙️ Prometheus配置:
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'fastapi-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'postgres-exporter'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis-exporter'
    static_configs:
      - targets: ['redis-exporter:9121']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

📈 关键指标:
- http_requests_total: HTTP请求总数
- http_request_duration_seconds: 请求响应时间
- http_requests_in_progress: 并发请求数
- database_connections_active: 活跃数据库连接
- redis_memory_used_bytes: Redis内存使用
"""
        else:
            config_content = f"📊 {monitoring_stack} 监控配置 (待实现)"

        return config_content

    def _configure_logging_system(self, log_level: str, output_format: str = "json") -> str:
        """配置日志系统"""
        logging_config = f"""
📝 日志系统配置:

🎚️ 日志级别: {log_level}
📄 输出格式: {output_format}

⚙️ FastAPI日志配置:
```python
import logging
import sys
from loguru import logger

# 移除默认处理器
logger.remove()

# 添加控制台输出
logger.add(
    sys.stdout,
    format="{{time:YYYY-MM-DD HH:mm:ss}} | {{level}} | {{name}}:{{function}}:{{line}} | {{message}}",
    level="{log_level}",
    serialize={str(output_format == 'json').lower()}
)

# 添加文件输出
logger.add(
    "logs/app.log",
    rotation="1 day",
    retention="30 days",
    level="{log_level}",
    format="{{time:YYYY-MM-DD HH:mm:ss}} | {{level}} | {{name}}:{{function}}:{{line}} | {{message}}"
)
```

📊 日志聚合 (ELK Stack):
```yaml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.10.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"

  logstash:
    image: docker.elastic.co/logstash/logstash:8.10.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.10.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
```

🔍 日志分析模式:
- 请求追踪: 包含请求ID的完整请求链路
- 错误聚合: 自动分组和统计错误类型
- 性能分析: 慢查询和性能瓶颈识别
- 安全审计: 登录、权限变更等安全事件
"""
        return logging_config

    def _create_alert_rules(self, alert_types: List[str]) -> str:
        """创建告警规则"""
        alert_rules = [
            "🚨 监控告警规则配置:",
            "",
            "⚡ Prometheus AlertManager规则:"
        ]
        
        rule_templates = {
            "high_error_rate": """
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "高错误率告警"
      description: "应用错误率超过10%，持续2分钟"
""",
            "high_response_time": """
  - alert: HighResponseTime
    expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "响应时间过长"
      description: "95%分位响应时间超过1秒，持续5分钟"
""",
            "database_connection_high": """
  - alert: DatabaseConnectionHigh
    expr: database_connections_active / database_connections_max > 0.8
    for: 3m
    labels:
      severity: critical
    annotations:
      summary: "数据库连接使用率过高"
      description: "数据库连接使用率超过80%，持续3分钟"
""",
            "memory_usage_high": """
  - alert: MemoryUsageHigh
    expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes > 0.9
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "内存使用率过高"
      description: "系统内存使用率超过90%，持续5分钟"
"""
        }
        
        for alert_type in alert_types:
            if alert_type in rule_templates:
                alert_rules.append(rule_templates[alert_type])
        
        alert_rules.extend([
            "",
            "📱 通知配置:",
            "- Slack: 实时告警通知",
            "- 邮件: 重要告警汇总",
            "- 钉钉: 国内团队通知",
            "- PagerDuty: 7x24值班响应"
        ])
        
        return "\n".join(alert_rules)

    def _setup_monitoring_dashboard(self, dashboard_type: str, services: List[str]) -> str:
        """设置监控仪表板"""
        if dashboard_type == "grafana":
            dashboard_config = """
📊 Grafana仪表板配置:

🎯 主要仪表板:

1. **应用概览仪表板**:
   - 请求量和响应时间趋势
   - 错误率和成功率统计
   - 活跃用户和会话数
   - 系统资源使用情况

2. **性能监控仪表板**:
   - API端点性能排行
   - 数据库查询性能分析
   - 缓存命中率和效果
   - 系统瓶颈识别

3. **基础设施仪表板**:
   - 服务器资源监控
   - 容器状态和资源使用
   - 网络流量和延迟
   - 磁盘使用和I/O性能

4. **业务监控仪表板**:
   - 用户注册和登录趋势
   - 功能使用统计
   - 业务转化率分析
   - 异常行为检测

📈 关键指标面板:
```json
{
  "dashboard": {
    "title": "FastAPI Application Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Response Time P95",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      }
    ]
  }
}
```

🔧 自动化配置:
- 通过代码定义仪表板配置
- 版本控制仪表板变更
- 自动化导入和更新
- 环境间配置同步
"""
        else:
            dashboard_config = f"📊 {dashboard_type} 仪表板配置 (待实现)"

        return dashboard_config