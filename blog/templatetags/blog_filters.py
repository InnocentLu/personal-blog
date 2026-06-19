"""blog 应用自定义模板标签与过滤器"""
from django import template

register = template.Library()


@register.filter
def split(value, arg):
    """
    将字符串按指定分隔符切分为列表
    用法：{{ value|split:"," }}
    """
    if not value:
        return []
    return value.split(arg)
