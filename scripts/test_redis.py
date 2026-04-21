import redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_url = os.getenv("REDIS_URL")

def test_redis_connection():
    try:
        redis_client = redis.Redis.from_url(redis_url)
        redis_client.lpush("test_list", "Hello, Redis!")
        value = redis_client.lpop("test_list").decode("utf-8")

        assert value == "Hello, Redis!"
        print("Redis connection test passed!")

    except Exception as e:
        print(f"Redis connection test failed: {e}")

if __name__ == "__main__":
    test_redis_connection()
