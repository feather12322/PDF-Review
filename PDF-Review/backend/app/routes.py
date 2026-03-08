from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from app.services.pdf_parser import PDFParser
from app.services.ai_extractor import AIExtractor
from app.services.matcher import ResumeMatcher
from app.utils.response import success_response, error_response
from app.utils.cache import CacheManager

api_bp = Blueprint('api', __name__)

pdf_parser = PDFParser()
ai_extractor = AIExtractor()
matcher = ResumeMatcher()
cache_manager = CacheManager()

# 存储解析结果（生产环境应使用数据库）
resume_storage = {}

@api_bp.route('/resume/upload', methods=['POST'])
def upload_resume():
    """上传并解析简历"""
    try:
        if 'file' not in request.files:
            return error_response('没有上传文件', 400)
        
        file = request.files['file']
        if file.filename == '':
            return error_response('文件名为空', 400)
        
        if not file.filename.lower().endswith('.pdf'):
            return error_response('只支持 PDF 格式', 400)
        
        # 生成唯一 ID
        resume_id = str(uuid.uuid4())
        
        # 保存文件
        filename = secure_filename(f"{resume_id}.pdf")
        from flask import current_app
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 解析 PDF
        raw_text = pdf_parser.parse(filepath)
        
        # 存储原始文本
        resume_storage[resume_id] = {
            'raw_text': raw_text,
            'filepath': filepath
        }
        
        return success_response({
            'resume_id': resume_id,
            'raw_text': raw_text[:500] + '...' if len(raw_text) > 500 else raw_text,
            'text_length': len(raw_text)
        }, '上传成功')
        
    except Exception as e:
        return error_response(f'上传失败: {str(e)}', 500)


@api_bp.route('/resume/extract', methods=['POST'])
def extract_info():
    """提取简历关键信息"""
    try:
        data = request.get_json()
        resume_id = data.get('resume_id')
        
        if not resume_id or resume_id not in resume_storage:
            return error_response('简历不存在', 404)
        
        # 检查缓存
        cached_data = cache_manager.get(f'extract:{resume_id}')
        if cached_data:
            return success_response(cached_data, '提取成功（缓存）')
        
        # 提取信息
        raw_text = resume_storage[resume_id]['raw_text']
        extracted_info = ai_extractor.extract_info(raw_text)
        
        result = {
            'resume_id': resume_id,
            **extracted_info
        }
        
        # 存储提取结果
        resume_storage[resume_id]['extracted_info'] = extracted_info
        
        # 缓存结果
        cache_manager.set(f'extract:{resume_id}', result, expire=86400)
        
        return success_response(result, '提取成功')
        
    except Exception as e:
        return error_response(f'提取失败: {str(e)}', 500)


@api_bp.route('/resume/match', methods=['POST'])
def match_resume():
    """简历与岗位匹配"""
    try:
        data = request.get_json()
        resume_id = data.get('resume_id')
        job_description = data.get('job_description')
        
        if not resume_id or resume_id not in resume_storage:
            return error_response('简历不存在', 404)
        
        if not job_description:
            return error_response('岗位描述不能为空', 400)
        
        # 检查缓存
        cache_key = f'match:{resume_id}:{hash(job_description)}'
        cached_data = cache_manager.get(cache_key)
        if cached_data:
            return success_response(cached_data, '匹配成功（缓存）')
        
        # 获取提取的信息
        extracted_info = resume_storage[resume_id].get('extracted_info')
        if not extracted_info:
            return error_response('请先提取简历信息', 400)
        
        # 执行匹配
        match_result = matcher.match(extracted_info, job_description)
        
        result = {
            'resume_id': resume_id,
            **match_result
        }
        
        # 缓存结果
        cache_manager.set(cache_key, result, expire=3600)
        
        return success_response(result, '匹配成功')
        
    except Exception as e:
        return error_response(f'匹配失败: {str(e)}', 500)


@api_bp.route('/resume/<resume_id>', methods=['GET'])
def get_resume(resume_id):
    """获取简历详情"""
    try:
        if resume_id not in resume_storage:
            return error_response('简历不存在', 404)
        
        resume_data = resume_storage[resume_id]
        
        return success_response({
            'resume_id': resume_id,
            'raw_text': resume_data.get('raw_text', ''),
            'extracted_info': resume_data.get('extracted_info', {})
        }, '获取成功')
        
    except Exception as e:
        return error_response(f'获取失败: {str(e)}', 500)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return success_response({'status': 'ok'}, 'Service is running')
