"""
my_blog 项目初始化文件
本地环境：使用 pymysql 作为 MySQL 驱动
云端环境：使用 psycopg2 作为 PostgreSQL 驱动（无需 pymysql）
"""
import os

# 仅在本地 MySQL 环境下注册 pymysql
if not os.getenv('DATABASE_URL'):
    import pymysql
    pymysql.install_as_MySQLdb()
