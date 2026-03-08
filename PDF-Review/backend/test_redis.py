"""
测试 Redis 连接和缓存功能
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("Redis 连接测试")
print("=" * 60)
print()

# 获取 Redis 配置
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_password = os.getenv('REDIS_PASSWORD', None)

print(f"Redis 配置:")
print(f"  Host: {redis_host}")
print(f"  Port: {redis_port}")
print(f"  Password: {'已设置' if redis_password else '未设置'}")
print()

# 测试连接
print("正在测试 Redis 连接...")
try:
    import redis
    
    r = redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password,
        decode_responses=True
    )
    
    # Ping 测试
    r.ping()
    print("✅ Redis 连接成功！")
    print()
    
    # 测试基本操作
    print("测试基本操作:")
    
    # 设置值
    test_key = "test:resume:123"
    test_value = {"name": "测试", "score": 85}
    
    import json
    r.setex(test_key, 60, json.dumps(test_value))
    print(f"✅ 写入测试数据: {test_key}")
    
    # 读取值
    cached = r.get(test_key)
    if cached:
        data = json.loads(cached)
        print(f"✅ 读取测试数据: {data}")
    
    # 删除值
    r.delete(test_key)
    print(f"✅ 删除测试数据")
    
    print()
    print("=" * 60)
    print("✅ Redis 缓存功能正常！")
    print("=" * 60)
    
except ImportError:
    print("❌ 未安装 redis 库")
    print()
    print("请安装:")
    print("  pip install redis")
    
except redis.exceptions.ConnectionError as e:
    print(f"❌ Redis 连接失败: {e}")
    print()
    print("可能的原因:")
    print("1. Redis 服务未启动")
    print("2. 连接配置不正确")
    print("3. 防火墙阻止连接")
    print()
    print("解决方案:")
    print("Windows:")
    print("  - 检查 Redis 服务是否运行")
    print("  - 打开服务管理器，查找 Redis 服务")
    print("  - 或在命令行运行: redis-server")
    print()
    print("验证 Redis:")
    print("  redis-cli ping")
    print("  应该返回: PONG")
    
except Exception as e:
    print(f"❌ 错误: {type(e).__name__}: {e}")

print()
