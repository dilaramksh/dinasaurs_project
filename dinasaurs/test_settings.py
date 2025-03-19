from pathlib import Path

class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # SQLite is much faster than Postgres for tests
        "NAME": ":memory:",  # Use in-memory DB for tests
    }
}

MIGRATION_MODULES = DisableMigrations()  # Disable migrations
DEBUG = False  # Ensure debug mode is off

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'storages',
    'social_media',  # Your custom app
]

# Use in-memory SQLite for fast tests and avoid network calls
DATABASES['default']['TEST'] = {
    'NAME': ':memory:',  # In-memory database for tests
}

# Disable AWS S3 during tests since it's not needed
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# MIDDLEWARE should be minimal for tests
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# TEMPLATES configuration for testing purposes
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

ROOT_URLCONF = 'dinasaurs.urls'
WSGI_APPLICATION = 'dinasaurs.wsgi.application'

# Authentication settings
AUTH_USER_MODEL = 'social_media.User'
LOGIN_URL = 'log_in'
REDIRECT_URL_WHEN_LOGGED_IN = 'dashboard'
DEFAULT_PROFILE_PICTURE = "profile_pictures/default.jpg"

# Password validators for testing (can be more lenient in tests)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

# Static files for testing (you can mock or disable this if needed)
STATIC_URL = '/static/'

# Time Zone and Language settings for consistency
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
