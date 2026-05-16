from redis import Redis
import os

host = os.environ.get('REDIS_HOST', 'localhost')
password = os.environ.get('REDIS_PASSWORD', 'YourPW')

rconn = Redis(host=host, port=6379, decode_responses=True, password=password)