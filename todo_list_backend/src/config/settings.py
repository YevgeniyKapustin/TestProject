"""
Django settings for todo_list_backend.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

from typing import Any, List
from pydantic_settings import BaseSettings


class DjangoSettings(BaseSettings):
    """Manage all the project settings"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DATABASES: dict = self.__get_databases()
        self.SIMPLE_JWT: dict = self.__set_settings_for_jwt()

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    SECRET_KEY: str
    DEBUG: bool

    ALLOWED_HOSTS: List[str]
    RATE_LIMIT: int
    TIME_ZONE: str

    LANGUAGE_CODE: str = 'ru'
    USE_I18N: bool = True
    USE_TZ: bool = True

    INSTALLED_APPS: list[str] = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'rest_framework',
        'rest_framework_simplejwt',

        'user',
        'task',
    ]

    MIDDLEWARE: list[str] = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',

        'middleware.RateLimitMiddleware'
    ]

    ROOT_URLCONF: str = 'config.urls'

    TEMPLATES: list[dict] = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

    WSGI_APPLICATION: str = 'config.wsgi.application'

    POSTGRES_ENGINE: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    DATABASES: dict = {'default': None}

    AUTH_PASSWORD_VALIDATORS: list[dict] = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    RQ_QUEUES: dict = {
        'default': {
            'URL': 'redis://localhost:6379/0',
            'DEFAULT_TIMEOUT': 360,
        }
    }

    REST_FRAMEWORK: dict = {
        'DEFAULT_RENDER_CLASSES': [
            'rest_framework.renderers.JSONRender',
            'rest_framework.renderers.BrowsableAPIRender',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework_simplejwt.authentication.JWTAuthentication'
        ]
    }
    SIMPLE_JWT: dict = {}

    STATIC_URL: str = 'static/'
    STATIC_ROOT: str = os.path.join(BASE_DIR, 'static')
    STATICFILES_DIRS: list = [os.path.join(BASE_DIR, 'src/static')]

    MEDIA_URL: str = 'media/'
    MEDIA_ROOT: str = os.path.join(BASE_DIR, 'media')

    DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'

    AUTH_USER_MODEL: str = 'user.CustomUser'

    def __get_databases(self) -> dict:
        return {
            'default': {
                'ENGINE': self.POSTGRES_ENGINE,
                'NAME': self.POSTGRES_DB,
                'USER': self.POSTGRES_USER,
                'PASSWORD': self.POSTGRES_PASSWORD,
                'HOST': self.POSTGRES_HOST,
                'PORT': self.POSTGRES_PORT
            }
        }

    def __set_settings_for_jwt(self) -> dict:
        return {
            "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
            "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
            "ROTATE_REFRESH_TOKENS": False,
            "BLACKLIST_AFTER_ROTATION": False,
            "UPDATE_LAST_LOGIN": False,

            "ALGORITHM": "HS256",
            "SIGNING_KEY": self.SECRET_KEY,
            "VERIFYING_KEY": "",
            "AUDIENCE": None,
            "ISSUER": None,
            "JSON_ENCODER": None,
            "JWK_URL": None,
            "LEEWAY": 0,

            "AUTH_HEADER_TYPES": ("Bearer",),
            "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
            "USER_ID_FIELD": "id",
            "USER_ID_CLAIM": "user_id",
            "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

            "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
            "TOKEN_TYPE_CLAIM": "token_type",
            "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

            "JTI_CLAIM": "jti",

            "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
            "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
            "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

            "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
            "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
            "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
            "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
            "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
            "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
        }

    class Config:
        env_file: str = '../.env'
        env_file_encoding: str = 'utf-8'


_settings: dict = DjangoSettings().dict()


def __dir__() -> List[str]:
    """The list of available options from DjangoSettings object."""
    return list(_settings.keys())


def __getattr__(name: str) -> Any:
    """Turn the module access into a DjangoSettings access."""
    return _settings[name]
