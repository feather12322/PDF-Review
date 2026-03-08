import os
import json
import re
from openai import OpenAI

class AIExtractor:
    """AI 信息提取服务"""
    
    def __init__(self):
        # 使用 DeepSeek API - 从环境变量读取
        api_key = os.getenv('DEEPSEEK_API_KEY')
        base_url = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
        
        if not api_key:
            print("警告: 未配置 DEEPSEEK_API_KEY 环境变量，将使用模拟数据")
            print("请设置环境变量: DEEPSEEK_API_KEY=your-api-key")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
            print(f"DeepSeek API 已配置 (Base URL: {base_url})")
    
    def extract_info(self, resume_text):
        """从简历文本中提取关键信息"""
        
        # 如果没有配置 API，返回模拟数据
        if not self.client:
            return self._extract_mock(resume_text)
        
        try:
            prompt = self._build_prompt(resume_text)
            
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的简历解析助手，擅长从简历中提取结构化信息。"},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"AI 提取失败，使用备用方案: {str(e)}")
            return self._extract_mock(resume_text)
    
    def _build_prompt(self, resume_text):
        """构建提取 Prompt"""
        return f"""
请从以下简历文本中提取关键信息，以 JSON 格式返回。

简历文本：
{resume_text[:2000]}

请提取以下信息：
1. 基本信息：姓名、电话、邮箱、地址
2. 求职信息：求职意向、期望薪资
3. 背景信息：工作年限、学历背景、技能列表、项目经历

返回格式（必须是有效的 JSON）：
{{
  "basic_info": {{
    "name": "姓名",
    "phone": "电话",
    "email": "邮箱",
    "address": "地址"
  }},
  "job_intention": {{
    "position": "期望岗位",
    "salary": "期望薪资"
  }},
  "background": {{
    "work_years": 工作年限数字,
    "education": "学历信息",
    "skills": ["技能1", "技能2"],
    "projects": ["项目1", "项目2"]
  }}
}}

注意：
- 如果某个字段无法提取，请填写空字符串或空数组
- work_years 必须是数字
- 确保返回的是有效的 JSON 格式
"""
    
    def _extract_mock(self, resume_text):
        """模拟提取（用于演示或 API 不可用时）"""
        import re
        
        # 简单的正则提取
        name = self._extract_name(resume_text)
        phone = self._extract_phone(resume_text)
        email = self._extract_email(resume_text)
        
        return {
            "basic_info": {
                "name": name or "未识别",
                "phone": phone or "未识别",
                "email": email or "未识别",
                "address": "未识别"
            },
            "job_intention": {
                "position": "未识别",
                "salary": "未识别"
            },
            "background": {
                "work_years": 0,
                "education": "未识别",
                "skills": [],
                "projects": []
            }
        }
    
    def _extract_name(self, text):
        """提取姓名"""
        patterns = [
            r'姓名[：:]\s*([^\s\n]{2,4})',
            r'Name[：:]\s*([A-Za-z\s]{2,20})',
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        return None
    
    def _extract_phone(self, text):
        """提取电话"""
        pattern = r'1[3-9]\d{9}'
        match = re.search(pattern, text)
        return match.group(0) if match else None
    
    def _extract_email(self, text):
        """提取邮箱"""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(pattern, text)
        return match.group(0) if match else None
