from redis import Redis
from django_redis import get_redis_connection
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse


# 给redis添加数据

# redis = Redis(host='localhost', port=32768, password='redispw', db=0)
# redis.set('name', 'zhangsan')
#
# # 从redis获取数据
# name = redis.get('name')
# print(name)


# 使用django-redis 添加数据和获取数据
redis = get_redis_connection('default')
redis.set('name', 'lisi')
name = redis.get('name')
print(name)