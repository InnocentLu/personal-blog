"""ASGI 配置文件，用于异步部署"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_blog.settings')

application = get_asgi_application()
