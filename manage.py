#!/usr/bin/env python
"""Django 项目管理脚本"""
import os
import sys


def main():
    """运行管理命令的入口函数"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_blog.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "无法导入 Django，请确认已安装 Django 并激活虚拟环境。"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
