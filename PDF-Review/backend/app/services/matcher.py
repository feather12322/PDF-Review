import re
from typing import Dict, List

class ResumeMatcher:
    """简历匹配服务"""
    
    def match(self, resume_data: Dict, job_description: str) -> Dict:
        """计算简历与岗位的匹配度"""
        
        # 提取岗位关键词
        job_keywords = self._extract_job_keywords(job_description)
        
        # 提取简历技能
        resume_skills = resume_data.get('background', {}).get('skills', [])
        
        # 计算各项匹配度
        skill_score = self._calculate_skill_match(resume_skills, job_keywords)
        experience_score = self._calculate_experience_match(resume_data, job_description)
        education_score = self._calculate_education_match(resume_data, job_description)
        
        # 综合评分（加权平均）
        total_score = (
            skill_score * 0.5 +
            experience_score * 0.3 +
            education_score * 0.2
        )
        
        # 匹配的关键词
        matched_keywords = self._find_matched_keywords(resume_skills, job_keywords)
        
        # 生成建议
        suggestions = self._generate_suggestions(total_score, skill_score, experience_score)
        
        return {
            "match_score": round(total_score, 2),
            "details": {
                "skill_match": round(skill_score, 2),
                "experience_match": round(experience_score, 2),
                "education_match": round(education_score, 2)
            },
            "matched_keywords": matched_keywords,
            "suggestions": suggestions
        }
    
    def _extract_job_keywords(self, job_description: str) -> List[str]:
        """从岗位描述中提取关键词"""
        # 常见技术关键词
        tech_keywords = [
            'Python', 'Java', 'JavaScript', 'Go', 'C++', 'C#',
            'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask', 'Spring',
            'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch',
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'Linux',
            'Git', 'CI/CD', 'Agile', 'Scrum',
            '机器学习', '深度学习', '数据分析', '算法', '架构设计'
        ]
        
        found_keywords = []
        job_lower = job_description.lower()
        
        for keyword in tech_keywords:
            if keyword.lower() in job_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def _calculate_skill_match(self, resume_skills: List[str], job_keywords: List[str]) -> float:
        """计算技能匹配度"""
        if not job_keywords:
            return 50.0  # 无法判断时给中等分
        
        if not resume_skills:
            return 20.0  # 简历无技能信息
        
        # 转换为小写进行比较
        resume_skills_lower = [s.lower() for s in resume_skills]
        job_keywords_lower = [k.lower() for k in job_keywords]
        
        # 计算匹配数量
        matched_count = sum(1 for keyword in job_keywords_lower 
                          if any(keyword in skill for skill in resume_skills_lower))
        
        # 匹配率
        match_rate = matched_count / len(job_keywords)
        
        # 转换为 0-100 分
        return match_rate * 100
    
    def _calculate_experience_match(self, resume_data: Dict, job_description: str) -> float:
        """计算经验匹配度"""
        work_years = resume_data.get('background', {}).get('work_years', 0)
        
        # 从岗位描述中提取年限要求
        required_years = self._extract_required_years(job_description)
        
        if required_years == 0:
            return 70.0  # 无明确要求时给较高分
        
        if work_years >= required_years:
            return 100.0
        elif work_years >= required_years * 0.7:
            return 80.0
        elif work_years >= required_years * 0.5:
            return 60.0
        else:
            return 40.0
    
    def _extract_required_years(self, job_description: str) -> int:
        """从岗位描述中提取年限要求"""
        patterns = [
            r'(\d+)\s*年以上',
            r'(\d+)\+\s*years',
            r'(\d+)\s*years?\s*of\s*experience'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, job_description, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return 0
    
    def _calculate_education_match(self, resume_data: Dict, job_description: str) -> float:
        """计算学历匹配度"""
        education = resume_data.get('background', {}).get('education', '').lower()
        job_lower = job_description.lower()
        
        # 学历等级
        education_levels = {
            '博士': 5, 'phd': 5, 'doctor': 5,
            '硕士': 4, 'master': 4,
            '本科': 3, 'bachelor': 3, '学士': 3,
            '专科': 2, 'associate': 2,
            '高中': 1, 'high school': 1
        }
        
        # 获取简历学历等级
        resume_level = 0
        for key, level in education_levels.items():
            if key in education:
                resume_level = max(resume_level, level)
        
        # 获取岗位要求学历等级
        required_level = 0
        for key, level in education_levels.items():
            if key in job_lower:
                required_level = max(required_level, level)
        
        if required_level == 0:
            return 80.0  # 无明确要求
        
        if resume_level >= required_level:
            return 100.0
        elif resume_level >= required_level - 1:
            return 70.0
        else:
            return 50.0
    
    def _find_matched_keywords(self, resume_skills: List[str], job_keywords: List[str]) -> List[str]:
        """找出匹配的关键词"""
        matched = []
        resume_skills_lower = [s.lower() for s in resume_skills]
        
        for keyword in job_keywords:
            if any(keyword.lower() in skill for skill in resume_skills_lower):
                matched.append(keyword)
        
        return matched
    
    def _generate_suggestions(self, total_score: float, skill_score: float, experience_score: float) -> str:
        """生成匹配建议"""
        if total_score >= 80:
            return "候选人综合匹配度高，强烈推荐安排面试"
        elif total_score >= 60:
            if skill_score < 60:
                return "候选人经验尚可，但技能匹配度偏低，建议进一步评估技术能力"
            else:
                return "候选人匹配度良好，建议安排面试"
        elif total_score >= 40:
            return "候选人基本符合要求，但存在一定差距，可作为备选"
        else:
            return "候选人与岗位匹配度较低，不建议优先考虑"
