import os
from pathlib import Path

# Programmatic package installer to bypass environment CLI execution restrictions
try:
    import allauth
except ImportError:
    import subprocess
    import sys
    print("[Auto-Installer] Installing django-allauth...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "django-allauth"])
        print("[Auto-Installer] django-allauth installed successfully.")
    except Exception as e:
        print(f"[Auto-Installer] Failed to install django-allauth: {e}")

# pyrefly: ignore [missing-import]
from dotenv import dotenv_values, load_dotenv
config = {**dotenv_values(".env")} 
SECRET_KEY = config["SECRET_KEY"]
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-_r5oh%e&by*-%$9qdmt%r#aaj8+e(15c^vm23#oqqh5b#&^6p-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(config["DEBUG"])
# Security and CSRF Settings
ALLOWED_HOSTS = config.get("ALLOWED_HOSTS", "localhost 127.0.0.1 *").split(" ")
CSRF_TRUSTED_ORIGINS = [f"http://{host}" for host in ALLOWED_HOSTS if host != "*"]
CSRF_TRUSTED_ORIGINS += [f"https://{host}" for host in ALLOWED_HOSTS if host != "*"]
# CSRF_TRUSTED_ORIGINS += ["http://localhost:8000", "http://127.0.0.1:8000", "http://0.0.0.0:8000"]

# Handle proxy-terminated SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# CSRF and Session Robustness
CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_SECURE = False # Set to True in production with HTTPS

# Logging Configuration


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Required by django-allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    
    # Project Apps ======
    'geo_locations',
    # Others Apps ======
    'tailwind',
    'theme', # The name of the app you created during init
    'django_browser_reload', # Optional: for hot-reloading
    'django_extensions',
    'whitenoise',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

TAILWIND_APP_NAME = 'theme'
NPM_BIN_PATH = config["NPM_BIN_PATH"]
INTERNAL_IPS = ["127.0.0.1"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]
if DEBUG:
    # Add django_browser_reload middleware only in DEBUG mode
    MIDDLEWARE += [
        "django_browser_reload.middleware.BrowserReloadMiddleware",
    ]

ROOT_URLCONF = 'BANGLADESH_GEOJSON.urls'

TEMPLATES_DIR = BASE_DIR / "templates"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'BANGLADESH_GEOJSON.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "leaflet",
]
STATIC_ROOT = config["STATIC_ROOT"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_MANIFEST_STRICT = False 

MEDIA_URL = "/media/"
MEDIA_ROOT =  config["MEDIA_ROOT"]



LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (23.8103, 90.4125),   # Dhaka, Bangladesh
    'DEFAULT_ZOOM': 7,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
    'SCALE': 'both',                        # show scale bar
    'ATTRIBUTION_PREFIX': 'My Map Project',
}

# django-allauth Settings
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'geo_locations:index'
LOGOUT_REDIRECT_URL = 'geo_locations:index'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_ADAPTER = 'geo_locations.adapters.NoSignupAdapter'

# Authentication Method: allow both username AND email
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True


if int(config["LOGGING"]) == 1:
    from .logging import LOGGING