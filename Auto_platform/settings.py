from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# 跨域配置
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8081",  # 前端地址
]

SECRET_KEY = 'django-insecure-d$a6#f0#jyfp)2j!+m3ko=ma5qgc^gg^#x4e^1wsn8_zwmts3@'
DEBUG = True
ALLOWED_HOSTS = []

# 应用配置
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',  # JWT认证
    'core',
    'api',
    'ui',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 跨域中间件
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 自定义用户模型
AUTH_USER_MODEL = 'core.User'

# 静态文件配置（解决 staticfiles 依赖错误）
STATIC_URL = '/static/'  # 静态文件访问前缀
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # 生产环境静态文件收集目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # 开发环境静态文件存放目录
]

# 媒体文件配置（头像）
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 测试报告路径
REPORT_ROOT = os.path.join(BASE_DIR, 'reports')
if not os.path.exists(REPORT_ROOT):
    os.makedirs(REPORT_ROOT)

# DRF配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

ROOT_URLCONF = 'Auto_platform.urls'

# 数据库配置（默认SQLite）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # 必须保留这一行
        'DIRS': [],  # 模板文件目录（默认空即可）
        'APP_DIRS': True,  # 允许从应用内的 templates 目录加载模板
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# 统一所有模型的默认主键类型为 BigAutoField（支持更大整数范围）
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'