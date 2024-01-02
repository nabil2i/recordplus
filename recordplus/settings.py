"""
Django settings for recordplus project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

import openai
# import cloudinary
# import cloudinary.uploader
# import cloudinary.api
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# BASE_URL= config(BASE_URL)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

openai.api_key = config('OPENAI_API_KEY')

## CLOUDINARY configuration
# CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME')
# CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY')
# CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = config('DEBUG', default='False')

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

AUTH_USER_MODEL = 'core.User'

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 3rd party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'djoser',
    'corsheaders',
    'whitenoise.runserver_nostatic',
    'drf_yasg',
    
    # # all auth
    # 'django.contrib.sites',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.twitter',
    # 'allauth.socialaccount.providers.google',    
    
    # my apps
    'core',
    'record',
    # 'social_auth'
    
]

# SOCIALACCOUNT_LOGIN_ON_GET=True # skip one page when authenticating

# # Authentication URLs
# LOGIN_REDIRECT_URL = '/api/auth'
# # ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# LOGOUT_REDIRECT_URL = '/api/auth'

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         # For each OAuth based provider, either add a ``SocialApp``
#         # (``socialaccount`` app) containing the required client
#         # credentials, or list them here:
#         # 'APP': {
#         #     'client_id': config('GOOGLE_CLIENT_ID'),
#         #     'secret': config('GOOGLE_CLIENT_SECRET'),
#         #     'key': ''
#         # },
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         }
#     },
#     'facebook': {
#         'APP': {
#             'client_id': config('FACEBOOK_APP_ID'),
#             'secret': '',
#         }
#     },
#     'twitter': {
#         'APP': {
#             'consumer_key': config('TWITTER_API_KEY'),
#             'secret': config('TWITTER_CONSUMER_SECRET'),
#         }
#     },
# }

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # "allauth.account.middleware.AccountMiddleware",
]


ROOT_URLCONF = 'recordplus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'DIRS': [os.path.join(BASE_DIR, 'build')],
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

WSGI_APPLICATION = 'recordplus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME':  config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST':  config('DB_HOST'),
#         'PORT': config('DB_PORT')
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
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

CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOWED_ORIGINS = [
#     "http://34.207.165.115/",
#     "https://recordplus.onrender.com/",
#     "http://127.0.0.1:8000/",
#     "http://localhost:5173/"
# ]

# CORS_ALLOW_METHODS = [
#     "GET",
#     "POST",
#     "PUT",
#     "PATCH",
#     "DELETE",
#     "OPTIONS",
# ]

# CORS_ALLOW_HEADERS = [
#     "Accept",
#     "Content-Type",
#     "Authorization",
# ]

# CORS_ALLOW_CREDENTIALS = True

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'build/static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY': 'error',
    # 'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema', 
    # 'COERCE_DECIMAL_TO_STRING': False,
    'PAGE_SIZE':10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated'
    # ],
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ALGORITHM': 'HS256',
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS=True
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL="from@nab.com"

AUTHENTICATION_BACKENDS = [
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    ## `allauth` specific authentication methods, such as login by email
    # 'allauth.account.auth_backends.AuthenticationBackend',
    
]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS' : {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'email/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_CONFIRMATION_EMAIL': True,
    'SEND_ACTIVATION_EMAIL': True,
    'SET_USERNAME_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'SERIALIZERS': {
        'user_create': 'core.serializers.UserCreateSerializer',  
        'user': 'core.serializers.UserCreateSerializer',  
        'user_delete': 'core.serializers.UserDeleteSerializer',  
    },
}

# SPECTACULAR_SETTINGS = {
#     'TITLE': 'RECORD PLUS',
    
# }

CELERY_BROKER_URL = config('CELERY_BROKER_URL')
# CELERY_RESULT_BACKEND = 'rpc://'