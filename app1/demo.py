import redis
from django_redis import get_redis_connection
conn = redis.Redis(host='192.168.1.8', port=6379)
conn.set('ping', 'pong')
print(conn.get('ping'))


conn = get_redis_connection('default')
conn.set('ping', 'pong')
#print(conn.get('ping'))