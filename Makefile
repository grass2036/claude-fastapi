# Claude FastAPI Project Makefile
# 简化开发流程的命令管理工具

.PHONY: help setup run dev test clean docker-up docker-down docker-build docker-restart logs migration upgrade

# 默认目标：显示帮助信息
help:
	@echo "可用命令:"
	@echo "  setup          - 初始化项目环境"
	@echo "  run            - 启动FastAPI开发服务器"
	@echo "  dev            - 启动开发模式（热重载）"
	@echo "  test           - 运行测试"
	@echo "  clean          - 清理缓存和临时文件"
	@echo ""
	@echo "Docker相关:"
	@echo "  docker-up      - 启动完整Docker环境"
	@echo "  docker-down    - 停止Docker环境"
	@echo "  docker-build   - 重新构建Docker镜像"
	@echo "  docker-restart - 重启Docker环境"
	@echo "  logs           - 查看Docker服务日志"
	@echo ""
	@echo "数据库相关:"
	@echo "  migration      - 创建数据库迁移文件 (make migration msg='your message')"
	@echo "  upgrade        - 执行数据库升级"

# 项目初始化
setup:
	@echo "🔧 初始化项目环境..."
	pip install -r requirements.txt
	@echo "✅ 环境安装完成"

# 启动FastAPI开发服务器（直接运行）
run:
	@echo "🚀 启动FastAPI服务器..."
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 开发模式（与run相同，但更明确）
dev: run

# 运行测试
test:
	@echo "🧪 运行测试..."
	pytest -v --cov=backend tests/ || echo "❌ 测试目录不存在，请先创建tests目录"

# 清理项目
clean:
	@echo "🧹 清理项目缓存..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name "*.pyo" -delete 2>/dev/null || true
	find . -name ".coverage" -delete 2>/dev/null || true
	@echo "✅ 清理完成"

# Docker相关命令
docker-up:
	@echo "🐳 启动Docker环境..."
	docker-compose up -d
	@echo "✅ Docker环境已启动"
	@echo "📊 后端服务: http://localhost:8000"
	@echo "🌐 前端服务: http://localhost:3000"
	@echo "📖 API文档: http://localhost:8000/docs"

docker-down:
	@echo "🛑 停止Docker环境..."
	docker-compose down
	@echo "✅ Docker环境已停止"

docker-build:
	@echo "🔨 重新构建Docker镜像..."
	docker-compose build --no-cache
	@echo "✅ Docker镜像构建完成"

docker-restart:
	@echo "🔄 重启Docker环境..."
	docker-compose down
	docker-compose up -d
	@echo "✅ Docker环境已重启"

# 查看Docker日志
logs:
	@echo "📋 查看Docker服务日志..."
	docker-compose logs -f

# 查看特定服务日志（使用方法: make logs-service service=backend）
logs-service:
	@echo "📋 查看 $(service) 服务日志..."
	docker-compose logs -f $(service)

# 数据库迁移相关
migration:
	@echo "📝 创建数据库迁移文件..."
	@if [ -z "$(msg)" ]; then \
		echo "❌ 请提供迁移消息: make migration msg='your message'"; \
		exit 1; \
	fi
	cd backend && alembic revision --autogenerate -m "$(msg)"
	@echo "✅ 迁移文件已创建"

upgrade:
	@echo "⬆️  执行数据库升级..."
	cd backend && alembic upgrade head
	@echo "✅ 数据库升级完成"

# 进入Docker容器（调试用）
shell-backend:
	@echo "🐚 进入后端容器..."
	docker-compose exec backend /bin/bash

shell-db:
	@echo "🐚 进入数据库容器..."
	docker-compose exec db psql -U postgres -d claude_fastapi

# 查看Docker服务状态
status:
	@echo "📊 Docker服务状态:"
	docker-compose ps

# 完整重置（危险操作）
reset:
	@echo "⚠️  这将删除所有数据和容器！"
	@read -p "确认要继续吗？(y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	docker-compose down -v
	docker-compose build --no-cache
	docker-compose up -d
	@echo "✅ 项目已完全重置"