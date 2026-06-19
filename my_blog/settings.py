"""
Django 项目核心配置文件
适配 Railway 平台 PostgreSQL 部署
敏感信息通过环境变量读取（Railway Variables / .env）
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 加载本地 .env 环境变量文件（Railway 上自动忽略，使用平台变量）
load_dotenv(BASE_DIR / '.env')

# 安全密钥（从环境变量 DJANGO_SECRET_KEY 读取）
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-default-key-for-dev-only')

# 调试模式（生产环境必须为 False）
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true'

# 允许访问的主机名（Railway 设置 DJANGO_ALLOWED_HOSTS=*）
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

# 中间件（WhiteNoise 必须放在 SecurityMiddleware 之后）
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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


# 数据库配置
# 云端（Railway）：使用 dj_database_url 解析 DATABASE_URL（PostgreSQL）
# 本地：从 .env 读取 MySQL 配置
_database_url = os.getenv('DATABASE_URL')
if _database_url:
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.config(
                default=_database_url,
                conn_max_age=600,
                ssl_require=True,
            )
        }
    except ImportError:
        # dj_database_url 未安装时手动解析
        from urllib.parse import urlparse
        _parsed = urlparse(_database_url)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': _parsed.path.lstrip('/'),
                'USER': _parsed.username or 'postgres',
                'PASSWORD': _parsed.password or '',
                'HOST': _parsed.hostname or 'localhost',
                'PORT': str(_parsed.port or 5432),
            }
        }
else:
    # 本地开发环境：使用 MySQL
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
# 生产环境静态文件收集目录（collectstatic 输出到此）
STATIC_ROOT = BASE_DIR / 'staticfiles'
# WhiteNoise 压缩静态文件存储（生产环境必需）
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# 媒体文件配置（用户上传的图片、视频）
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# 默认主键字段类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
