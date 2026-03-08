"""
API 测试脚本
用于测试后端接口是否正常工作
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_health():
    """测试健康检查"""
    print("测试健康检查...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_upload_resume(pdf_path):
    """测试上传简历"""
    print("测试上传简历...")
    with open(pdf_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/resume/upload", files=files)
    
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    if result['code'] == 200:
        return result['data']['resume_id']
    return None

def test_extract_info(resume_id):
    """测试信息提取"""
    print(f"\n测试信息提取 (resume_id: {resume_id})...")
    response = requests.post(
        f"{BASE_URL}/resume/extract",
        json={'resume_id': resume_id}
    )
    
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")

def test_match_resume(resume_id):
    """测试匹配评分"""
    print(f"\n测试匹配评分 (resume_id: {resume_id})...")
    
    job_description = """
    招聘 Python 后端工程师
    
    岗位要求：
    - 3 年以上 Python 开发经验
    - 熟悉 Django 或 Flask 框架
    - 熟悉 MySQL、Redis 等数据库
    - 有微服务架构经验优先
    - 本科及以上学历
    """
    
    response = requests.post(
        f"{BASE_URL}/resume/match",
        json={
            'resume_id': resume_id,
            'job_description': job_description
        }
    )
    
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")

if __name__ == '__main__':
    # 测试健康检查
    test_health()
    
    # 如果有测试 PDF 文件，可以测试完整流程
    # pdf_path = "test_resume.pdf"
    # resume_id = test_upload_resume(pdf_path)
    # if resume_id:
    #     test_extract_info(resume_id)
    #     test_match_resume(resume_id)
    
    print("\n提示: 要测试完整流程，请准备一个 PDF 简历文件，并取消注释上面的代码")
