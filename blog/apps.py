"""blog 应用配置"""
from django.apps import AppConfig


class BlogConfig(AppConfig):
    """blog 应用配置类"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = '个人博客'
