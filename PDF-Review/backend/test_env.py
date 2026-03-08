"""
环境变量测试脚本
用于验证 DeepSeek API 环境变量是否正确配置
"""

import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

print("=" * 50)
print("环境变量测试")
print("=" * 50)
print()

# 检查环境变量
api_key = os.getenv('DEEPSEEK_API_KEY')
base_url = os.getenv('DEEPSEEK_BASE_URL')

print("1. 检查环境变量配置:")
print("-" * 50)

if api_key:
    # 只显示前10个字符，保护隐私
    masked_key = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else api_key[:10] + "..."
    print(f"✅ DEEPSEEK_API_KEY: {masked_key}")
else:
    print("❌ DEEPSEEK_API_KEY: 未设置")

if base_url:
    print(f"✅ DEEPSEEK_BASE_URL: {base_url}")
else:
    print("⚠️  DEEPSEEK_BASE_URL: 未设置（将使用默认值）")

print()

# 测试 API 连接
if api_key:
    print("2. 测试 API 连接:")
    print("-" * 50)
    
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=api_key,
            base_url=base_url or 'https://api.deepseek.com'
        )
        
        print("正在连接 DeepSeek API...")
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": "Hello, please respond with 'OK' if you receive this message."}
            ],
            max_tokens=10
        )
        
        print(f"✅ API 连接成功")
        print(f"响应: {response.choices[0].message.content}")
        print(f"模型: {response.model}")
        
    except ImportError:
        print("⚠️  未安装 openai 库，跳过 API 测试")
        print("   运行: pip install openai")
    except Exception as e:
        print(f"❌ API 连接失败: {str(e)}")
        print("   请检查:")
        print("   1. API Key 是否正确")
        print("   2. 网络连接是否正常")
        print("   3. 是否能访问 https://api.deepseek.com")
else:
    print("2. 跳过 API 测试（未配置 API Key）")

print()
print("=" * 50)
print("测试完成")
print("=" * 50)
print()

# 给出建议
if not api_key:
    print("💡 建议:")
    print("   请设置 DEEPSEEK_API_KEY 环境变量")
    print()
    print("   Windows PowerShell:")
    print("   [System.Environment]::SetEnvironmentVariable('DEEPSEEK_API_KEY', 'your-key', 'User')")
    print()
    print("   Mac/Linux:")
    print("   export DEEPSEEK_API_KEY='your-key'")
    print()
    print("   或在 .env 文件中设置:")
    print("   DEEPSEEK_API_KEY=your-key")
