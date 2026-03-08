#!/bin/bash

echo "========================================"
echo "  智能简历分析系�?- 启动脚本"
echo "========================================"
echo ""

echo "[1/4] 检�?Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "�?未检测到 Python，请先安�?Python 3.9+"
    exit 1
fi
echo "�?Python 环境正常"

echo ""
echo "[2/4] 检�?Node.js 环境..."
if ! command -v node &> /dev/null; then
    echo "�?未检测到 Node.js，请先安�?Node.js 16+"
    exit 1
fi
echo "�?Node.js 环境正常"

echo ""
echo "[3/4] 启动后端服务..."
cd backend

if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate

if [ ! -f ".env" ]; then
    echo "⚠️  未找到 .env 文件，正在创建..."
    cat > .env << 'EOF'
# DeepSeek API 配置
# API Key 已设置为系统环境变量
# 如需覆盖，取消下行注释并填入 API Key
# DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com

# Redis 配置（可选）
REDIS_HOST=localhost
REDIS_PORT=6379

# 应用配置
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=10485760
EOF
    echo "✅ .env 文件已创建"
    echo "ℹ️  DeepSeek API Key 使用系统环境变量"
fi

echo "安装依赖..."
pip install -q -r requirements.txt

echo "启动后端..."
python main.py &
BACKEND_PID=$!

cd ..

echo ""
echo "[4/4] 启动前端服务..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "安装前端依赖（首次运行需要几分钟�?.."
    npm install
fi

echo "启动前端..."
npm run serve &
FRONTEND_PID=$!

cd ..

echo ""
echo "========================================"
echo "�?启动完成�?
echo ""
echo "后端地址: http://localhost:5000"
echo "前端地址: http://localhost:8080"
echo ""
echo "后端 PID: $BACKEND_PID"
echo "前端 PID: $FRONTEND_PID"
echo ""
echo "�?Ctrl+C 停止服务"
echo "========================================"
echo ""

# 等待用户中断
wait
