
import os
import sys
import django
from django_redis import get_redis_connection

from app1.utils.encrypt import md5
#导入django的配置文件
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 获取当前文件的上上级目录，这里就是项目的根目录
sys.path.append(base_dir)  # 将项目的根目录添加到环境变量中
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")  # 设置环境变量
django.setup() # 加载项目的配置，初始化django，这样才能使用django的settings

# 使用django-redis 添加数据和获取数据
redis = get_redis_connection('default')
redis.set('15088870678', '123456')

name = redis.get('15088870678')
print(name)
# 清空redis数据库
#redis.flushdb()