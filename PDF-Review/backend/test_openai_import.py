"""
测试 OpenAI 库导入
"""

print("正在测试 OpenAI 库导入...")

try:
    from openai import OpenAI
    print("✅ OpenAI 库导入成功")
    
    # 测试创建客户端
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv('DEEPSEEK_API_KEY')
    base_url = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
    
    if api_key:
        client = OpenAI(api_key=api_key, base_url=base_url)
        print(f"✅ OpenAI 客户端创建成功")
        print(f"   Base URL: {base_url}")
    else:
        print("⚠️  未配置 DEEPSEEK_API_KEY")
    
    print("\n所有测试通过！可以启动后端服务了。")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    print("\n请运行以下命令修复:")
    print('pip install "httpx<0.28" --upgrade')
