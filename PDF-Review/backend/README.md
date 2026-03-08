# 智能简历分析系统 - 后端

基于 Flask 的 RESTful API 服务，提供简历解析、信息提取和智能匹配功能。

## 功能特性

- PDF 简历上传与解析
- AI 驱动的关键信息提取
- 智能岗位匹配与评分
- Redis 缓存支持（可选）

## 快速开始

### 1. 安装依赖

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key
```

### 3. 运行服务

```bash
python main.py
```

服务将在 http://localhost:5000 启动

## API 文档

### 1. 上传简历
- **URL**: `/api/resume/upload`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **参数**: `file` (PDF 文件)

### 2. 提取信息
- **URL**: `/api/resume/extract`
- **Method**: `POST`
- **Body**: `{"resume_id": "uuid"}`

### 3. 匹配评分
- **URL**: `/api/resume/match`
- **Method**: `POST`
- **Body**: `{"resume_id": "uuid", "job_description": "岗位描述"}`

### 4. 获取简历详情
- **URL**: `/api/resume/<resume_id>`
- **Method**: `GET`
