import redis
from config import REDIS_HOST,REDIS_PORT

redis_db  = redis.Redis(host = f"{REDIS_HOST}",port = REDIS_PORT,decode_responses=True)

