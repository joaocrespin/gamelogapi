from redis import Redis
import env

rconn = Redis(host='localhost', port=6379, decode_responses=True, password=env.REDIS_PASSWORD)

