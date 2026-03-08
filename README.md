# AI 智能简历分析系统

基于 AI 大模型的智能简历解析与岗位匹配系统，自动提取简历关键信息并进行智能评分。

## 项目架构

```
PDF-Review/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── services/       # 核心业务逻辑
│   │   │   ├── pdf_parser.py      # PDF 解析
│   │   │   ├── ai_extractor.py    # AI 信息提取
│   │   │   └── matcher.py         # 智能匹配评分
│   │   ├── utils/          # 工具模块
│   │   │   ├── cache.py           # Redis 缓存
│   │   │   └── response.py        # 统一响应格式
│   │   └── routes.py       # API 路由
│   └── main.py             # 应用入口
│
└── frontend/               # 前端应用
    ├── src/
    │   ├── views/          # 页面组件
    │   ├── api/            # API 接口
    │   └── router/         # 路由配置
    └── vue.config.js       # Vue 配置
```

## 技术选型

### 后端技术栈
- **框架**: Flask 3.0.0
- **PDF 解析**: pdfplumber 0.10.3
- **AI 模型**: DeepSeek API / OpenAI
- **缓存**: Redis 5.0.1
- **跨域**: Flask-CORS 4.0.0

### 前端技术栈
- **框架**: Vue 3.3.4
- **UI 组件**: Element Plus 2.4.0
- **路由**: Vue Router 4.2.4
- **HTTP 客户端**: Axios 1.5.0

### 核心功能
- PDF 简历自动解析
- AI 智能信息提取（姓名、电话、邮箱、工作经历等）
- 岗位需求智能匹配与评分
- Redis 缓存优化性能

## 部署方式

### 本地开发部署

#### 快速启动（推荐）

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```cmd
start.bat
```

#### 手动启动

**1. 启动后端**
```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入 DEEPSEEK_API_KEY

# 启动服务
python main.py
```

后端服务运行在 `http://localhost:5000`

**2. 启动前端**
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run serve
```

前端应用运行在 `http://localhost:8080`

### 生产环境部署

#### 前端部署到 GitHub Pages

```bash
cd frontend

# 构建并部署
npm run deploy
```

访问地址: https://feather12322.github.io/PDF-Review

#### 后端部署选项

**方案一: Docker 部署**
```bash
docker-compose up -d
```

**方案二: 传统服务器**
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

**方案三: 阿里云 Serverless**
```bash
npm install -g @serverless-devs/s
s config add
s deploy
```

## 使用说明

### 环境变量配置

创建 `backend/.env` 文件：

```env
# DeepSeek API 配置
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com

# Redis 配置（可选）
REDIS_HOST=localhost
REDIS_PORT=6379

# 应用配置
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=10485760
```

### API 接口

**1. 上传简历**
```http
POST /api/resume/upload
Content-Type: multipart/form-data

参数: file (PDF 文件)
```

**2. 提取信息**
```http
POST /api/resume/extract
Content-Type: application/json

{
  "resume_id": "uuid"
}
```

**3. 匹配评分**
```http
POST /api/resume/match
Content-Type: application/json

{
  "resume_id": "uuid",
  "job_description": "岗位描述"
}
```

### 功能使用流程

1. 访问前端页面
2. 上传 PDF 格式简历
3. 系统自动解析并提取关键信息
4. 输入岗位描述进行智能匹配
5. 查看匹配评分和详细分析

## 系统要求

- Python 3.9+
- Node.js 16+
- Redis（可选，用于缓存）

## 许可证

MIT License
