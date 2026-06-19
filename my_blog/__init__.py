"""
my_blog 项目初始化文件
使用 pymysql 作为 MySQL 驱动，并将其伪装成 MySQLdb
以兼容 Django ORM 对 MySQLdb 的引用
"""
import pymysql

# 将 pymysql 注册为 MySQLdb，使 Django ORM 可正常使用 MySQL
pymysql.install_as_MySQLdb()
