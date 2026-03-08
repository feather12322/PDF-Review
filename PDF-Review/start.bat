@echo off
chcp 65001 >nul
echo ========================================
echo   智能简历分析系统 - 启动脚本
echo ========================================
echo.

echo [1/4] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到 Python，请先安装 Python 3.9+
    pause
    exit /b 1
)
echo ✅ Python 环境正常

echo.
echo [2/4] 检查 Node.js 环境...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到 Node.js，请先安装 Node.js 16+
    pause
    exit /b 1
)
echo ✅ Node.js 环境正常

echo.
echo [3/4] 启动后端服务...
cd backend

REM 指定 Anaconda 环境的 Python 路径
set PYTHON_PATH=C:\Users\zhousicheng\anaconda\envs\DGM4\python.exe

REM 检查指定的 Python 环境是否存在
if not exist "%PYTHON_PATH%" (
    echo ❌ 未找到指定的 Python 环境: %PYTHON_PATH%
    echo 请检查路径是否正确
    pause
    exit /b 1
)
echo ✅ 使用 Anaconda 环境: DGM4

REM 检查 .env 文件
if not exist .env (
    echo ⚠️  未找到 .env 文件，正在创建...
    echo # DeepSeek API 配置 > .env
    echo DEEPSEEK_API_KEY=sk-dcbb639c0ad145398bbd1839ab53e792 >> .env
    echo DEEPSEEK_BASE_URL=https://api.deepseek.com >> .env
    echo. >> .env
    echo # Redis 配置（可选） >> .env
    echo REDIS_HOST=localhost >> .env
    echo REDIS_PORT=6379 >> .env
    echo. >> .env
    echo # 应用配置 >> .env
    echo UPLOAD_FOLDER=uploads >> .env
    echo MAX_CONTENT_LENGTH=10485760 >> .env
    echo ✅ .env 文件已创建
) else (
    echo ✅ .env 文件已存在
)

echo 启动后端服务...
start "后端服务 - 智能简历分析系统" cmd /k ""%PYTHON_PATH%" main.py"

cd ..

echo.
echo [4/4] 启动前端服务...
cd frontend

if not exist node_modules (
    echo 安装前端依赖（首次运行需要几分钟）...
    call npm install
) else (
    echo ✅ 前端依赖已安装
)

echo 启动前端服务...
start "前端服务 - 智能简历分析系统" cmd /k "npm run serve"

cd ..

echo.
echo ========================================
echo ✅ 启动完成！
echo.
echo 后端地址: http://localhost:5000
echo 前端地址: http://localhost:8080
echo.
echo 请在浏览器中访问前端地址使用系统
echo ========================================
echo.
pause
