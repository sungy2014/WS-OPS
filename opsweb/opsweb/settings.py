"""
Django settings for opsweb project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 导入自定义工具包
sys.path.insert(0, os.path.join(BASE_DIR, 'utils'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')wl07)zwx1ou41mef(=@&1#9ru0bmt1)aeqb&%x3xnv1$d#dw@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'accounts',
    'dashboard',
    'resources',
    'monitor',
    'api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'opsweb.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'opsweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
os.path.join(BASE_DIR, "static"),
)
#STATIC_ROOT = os.path.join(BASE_DIR, "static")

# 定时任务配置
CRONJOBS = [  
    # 每隔2分钟运行下面的函数，使得 ServerModel 模型与阿里云上的ECS保持一致
    ('*/2 * * * *', 'resources.cron.ServerAliyunAutoAddCrontab'),
    ('*/10 * * * *', 'resources.cron.ServerAliyunAutoRefreshCrontab'),
    ('*/15 * * * *', 'resources.cron.CmdbAutoAddCrontab'),
    ('50 00 * * *', 'resources.cron.ServerStatisticByDayCrontab'),
    ('10 00 * * *', 'resources.cron.CmdbStatisticByDayCrontab'),
    ('55 23 * * *', 'monitor.cron.ZabbixHostSyncCrontab'),
]

# 日志配置
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False, 
    "loggers": {
        "info_logger": {
            "handlers": ["info_handler"],
            "level": "INFO",
            "propagate": False,
        },
        "error_logger": {
            "handlers": ["error_handler"],
            "level": "ERROR",
            "propagate": False,
        },
        "console_logger": {
            "handlers": ["console_handler"],
            "level": "DEBUG",
        },
    },
    "handlers": {
        "info_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR,'logs','wsops.log'),
            "when": "midnight",
            "backupCount": 7,
            "encoding": "utf8",
            "formatter": "verbose_format",
        },
        "error_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR,'logs','error.log'),
            "when": "midnight",
            "backupCount": 7,
            "encoding": "utf8",
            "formatter": "verbose_format",
        },
        "console_handler": {
            "class": "logging.StreamHandler",
            "formatter": "simple_format",
        },
    },
    "formatters": {
        "verbose_format": {
            "format": "%(asctime)s-[%(levelname)s]-%(pathname)s-[line:%(lineno)2d]-%(message)s"
        },
        "simple_format": {
            "format": "%(asctime)s-[%(levelname)s]-%(pathname)s-%(message)s"
        },
    },
    "root": {
        "handlers": ["info_handler"],
        "level": "INFO",
    },
}
