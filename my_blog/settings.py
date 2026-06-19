"""
Django 项目核心配置文件
配置数据库、模板、静态文件、媒体文件等
敏感信息通过 python-dotenv 从 .env 文件读取
支持本地 MySQL 和云端 PostgreSQL 自动切换
"""
import os
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 加载 .env 环境变量文件
load_dotenv(BASE_DIR / '.env')

# 安全密钥（从环境变量读取）
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-default-key')

# 调试模式（从环境变量读取，默认关闭）
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true'

# 允许访问的主机名（从环境变量读取）
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')

# 已安装的应用
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 本项目应用
    'blog',
]

# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 生产环境添加 WhiteNoise 中间件（静态文件服务）
try:
    import whitenoise.middleware
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
except ImportError:
    pass

# 根路由配置
ROOT_URLCONF = 'my_blog.urls'

# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 自定义上下文处理器：注入博主信息到所有模板
                'blog.context_processors.blog_info',
            ],
        },
    },
]

# WSGI 应用入口
WSGI_APPLICATION = 'my_blog.wsgi.application'


# 数据库配置：自动检测环境
# 云端（Railway）：通过 DATABASE_URL 环境变量使用 PostgreSQL
# 本地：通过 .env 配置使用 MySQL
database_url = os.getenv('DATABASE_URL')
if database_url:
    # 云端环境：解析 DATABASE_URL（格式：postgres://user:pass@host:port/dbname）
    parsed = urlparse(database_url)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parsed.path.lstrip('/'),
            'USER': parsed.username or 'postgres',
            'PASSWORD': parsed.password or '',
            'HOST': parsed.hostname or 'localhost',
            'PORT': str(parsed.port or 5432),
        }
    }
else:
    # 本地环境：使用 MySQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'my_weblog'),
            'USER': os.getenv('DB_USER', 'root'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }


# 密码验证规则
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# 国际化配置
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = False  # 关闭时区转换，使用本地时间


# 静态文件配置
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
# 生产环境静态文件收集目录
STATIC_ROOT = BASE_DIR / 'staticfiles'


# 媒体文件配置（用户上传的图片、视频）
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# 默认主键字段类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
