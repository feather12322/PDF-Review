import pdfplumber
import re

class PDFParser:
    """PDF 解析服务"""
    
    def parse(self, file_path):
        """解析 PDF 文件，提取文本"""
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            # 清洗文本
            cleaned_text = self.clean_text(text)
            return cleaned_text
            
        except Exception as e:
            raise Exception(f"PDF 解析失败: {str(e)}")
    
    def clean_text(self, text):
        """清洗文本"""
        if not text:
            return ""
        
        # 去除多余空格
        text = re.sub(r'\s+', ' ', text)
        
        # 去除特殊字符（保留中文、英文、数字、常用标点）
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s\.,;:!?()（）、，。；：！？\-\+@]', '', text)
        
        # 去除首尾空格
        text = text.strip()
        
        return text
