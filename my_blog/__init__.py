"""
my_blog 项目初始化文件
本地环境：使用 pymysql 作为 MySQL 驱动
云端环境（Railway）：使用 psycopg2 作为 PostgreSQL 驱动
"""
import os

# 本地 MySQL 环境需要注册 pymysql（DATABASE_URL 未设置时）
if not os.getenv('DATABASE_URL'):
    import pymysql
    pymysql.install_as_MySQLdb()
