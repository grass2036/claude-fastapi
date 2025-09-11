#!/bin/bash
cd /app
# 尝试导入，如果失败则使用备用路径
if python -c "import backend.main" 2>/dev/null; then
    exec uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
else
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
fi