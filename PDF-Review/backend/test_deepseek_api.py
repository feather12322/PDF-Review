"""
测试 DeepSeek API 连接
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

print("=" * 60)
print("DeepSeek API 连接测试")
print("=" * 60)
print()

# 获取配置
api_key = os.getenv('DEEPSEEK_API_KEY')
base_url = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')

print(f"API Key: {api_key[:10]}...{api_key[-4:] if api_key else 'None'}")
print(f"Base URL: {base_url}")
print()

if not api_key:
    print("❌ 未配置 DEEPSEEK_API_KEY")
    exit(1)

print("正在测试 API 连接...")
print()

try:
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    # 发送测试请求
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": "请回复：测试成功"}
        ],
        max_tokens=20
    )
    
    print("✅ API 连接成功！")
    print(f"响应: {response.choices[0].message.content}")
    print(f"模型: {response.model}")
    print()
    
except Exception as e:
    print(f"❌ API 连接失败")
    print(f"错误类型: {type(e).__name__}")
    print(f"错误信息: {str(e)}")
    print()
    
    # 提供解决建议
    if "Connection error" in str(e):
        print("💡 可能的原因:")
        print("1. 网络连接问题")
        print("2. 防火墙阻止")
        print("3. API 地址不正确")
        print("4. 需要代理访问")
        print()
        print("解决方案:")
        print("- 检查网络连接")
        print("- 尝试使用浏览器访问: https://api.deepseek.com")
        print("- 如需代理，设置环境变量:")
        print("  set HTTP_PROXY=http://proxy:port")
        print("  set HTTPS_PROXY=http://proxy:port")
    elif "API key" in str(e):
        print("💡 API Key 可能无效或已过期")
        print("请检查 .env 文件中的 DEEPSEEK_API_KEY")
    else:
        print("💡 其他错误，请查看详细错误信息")

print("=" * 60)
