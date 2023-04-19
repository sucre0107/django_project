import os
import sys
import django
from django_redis import get_redis_connection

from app1.utils.encrypt import md5



base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # 获取当前文件的上上级目录，这里就是项目的根目录
sys.path.append(base_dir)  # 将项目的根目录添加到环境变量中
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")  # 设置环境变量
django.setup() # 加载项目的配置，初始化django，这样才能使用django的ORM

from app1.models import Administrator, Customer

Customer.objects.create(username='admin', password=md5('admin'), active=1,level_id=1,creator_id=1)


