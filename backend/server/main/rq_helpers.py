
import redis
from rq import Queue
from server import config

# get redis connection
redis_connection = redis.from_url(config.DevelopmentConfig.REDIS_URL)

# get rq queue with redis connection
queue = Queue(connection=redis_connection)
