"""
Django 项目核心配置文件
适配 Railway 平台 PostgreSQL 部署
敏感信息通过环境变量读取（Railway Variables / .env）
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

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

# 中间件（WhiteNoise 必须放在 SecurityMiddleware 之后第一位）
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


# 数据库配置：使用 dj_database_url 解析 Railway 的 DATABASE_URL
# Railway 自动注入 DATABASE_URL（PostgreSQL 连接字符串）
# 注意：不启用 ssl_require，Railway 内部连接不支持 SSL
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
    )
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


# 静态文件配置（生产环境核心）
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
# collectstatic 收集目录（Railway 构建时生成）
STATIC_ROOT = BASE_DIR / 'staticfiles'
# WhiteNoise 压缩静态文件存储（生产环境必需，自动服务 /static/ 请求）
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# 媒体文件配置（用户上传的图片、视频）
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# 默认主键字段类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
