import os
import json

class CacheManager:
    """缓存管理器（简化版，生产环境应使用 Redis）"""
    
    def __init__(self):
        self.cache = {}
        self.use_redis = False
        
        # 尝试连接 Redis
        try:
            import redis
            redis_host = os.getenv('REDIS_HOST', 'localhost')
            redis_port = int(os.getenv('REDIS_PORT', 6379))
            redis_password = os.getenv('REDIS_PASSWORD', None)
            
            self.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                decode_responses=True
            )
            self.redis_client.ping()
            self.use_redis = True
            print("Redis 连接成功")
        except Exception as e:
            # Redis 不可用时静默降级到内存缓存
            # print(f"Redis 连接失败，使用内存缓存: {str(e)}")
            self.redis_client = None
    
    def get(self, key):
        """获取缓存"""
        try:
            if self.use_redis and self.redis_client:
                value = self.redis_client.get(key)
                return json.loads(value) if value else None
            else:
                return self.cache.get(key)
        except Exception as e:
            print(f"缓存获取失败: {str(e)}")
            return None
    
    def set(self, key, value, expire=3600):
        """设置缓存"""
        try:
            if self.use_redis and self.redis_client:
                self.redis_client.setex(key, expire, json.dumps(value))
            else:
                self.cache[key] = value
        except Exception as e:
            print(f"缓存设置失败: {str(e)}")
    
    def delete(self, key):
        """删除缓存"""
        try:
            if self.use_redis and self.redis_client:
                self.redis_client.delete(key)
            else:
                self.cache.pop(key, None)
        except Exception as e:
            print(f"缓存删除失败: {str(e)}")
