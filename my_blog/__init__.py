"""
my_blog 项目初始化文件
本地环境：使用 pymysql 作为 MySQL 驱动
云端环境：MySQL 用 pymysql，PostgreSQL 用 psycopg2
"""
import os

# 检测是否需要 pymysql（本地 MySQL 或云端 MySQL）
database_url = os.getenv('DATABASE_URL', '')
need_pymysql = (
    not database_url  # 本地无 DATABASE_URL，使用 MySQL
    or database_url.startswith('mysql')  # 云端 MySQL
)

if need_pymysql:
    import pymysql
    pymysql.install_as_MySQLdb()
