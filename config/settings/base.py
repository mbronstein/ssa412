"""
Base settings to build other settings files upon.
"""
from pathlib import Path
import environ
# from django.contrib.admin import site
# import adminactions.actions as actions

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent   # ssa412/
APPS_DIR = ROOT_DIR / "ssa412"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)  #mb changed default to true
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))

USE_TZ = env.bool("USE_TZ", default=True)
TIME_ZONE = env.bool("TIME_ZONE", default="UTC")
LANGUAGE_CODE = env.bool("LANGUAGE_CODE", default="en-us")
SITE_ID = env.str("SITE_ID", default=1)

DATABASES = {
    # see django-environ for env.db()
    'default': env.db(),
}

# URLS
ROOT_URLCONF = "config.urls"

# WSGI
WSGI_APPLICATION = "wsgi.application"

# APPS
DJANGO_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    # The following apps are required:
    'django.contrib.auth',
    'django.contrib.messages',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.forms",
    "grappelli",
    # "django.contrib.humanize", # Handy template tags
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "django_comments_xtd",
    "django_comments",
    "taggit",
    "django_extensions",
    "django_filters",
    "post_office",
    "import_export",
    "django_tables2",
    "adminactions",
    "axes",
    "todo",
    "request_logging",

    # "admin_auto_filters",
]

# MY APPS
LOCAL_APPS = [
    "ssa412.users.apps.UsersConfig",
    "ssoffices.apps.SsofficesConfig",
    "matters.apps.MattersConfig",
    "products.apps.ProductsConfig"

]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
MIGRATION_MODULES = {"sites": "ssa412.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    # for django-axes login logger
    'axes.backends.AxesBackend',
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL =  env("LOGIN_REDIRECT_URL", default='/')
LOGIN_URL = "account_login"


# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # can I leave this in even if toolbar not enabled?
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
]

# WhiteNoise
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa F405
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(APPS_DIR / "static")]

# MEDIA
MEDIA_ROOT = str(APPS_DIR / "media")
MEDIA_URL = "/media/"

# TEMPLATES
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR / "templates")],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "ssa412.utils.context_processors.settings_context",
            ],
        },
    }
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"

# FIXTURES
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
SECRET_KEY = env.str("SECRET_KEY")  # must be in .env (no default)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')  #must be in .env no default
SESSION_COOKIE_HTTPONLY = env.bool("SESSION_COOKIE_HTTPONLY", default=True)
CSRF_COOKIE_HTTPONLY = env.bool("CSRF_COOKIE_HTTPONLY", default=True)
SECURE_BROWSER_XSS_FILTER = env.bool("SECURE_BROWSER_XSS_FILTER", default=True)
X_FRAME_OPTIONS = env("X_FRAME_OPTIONS", default="DENY")


# SESSIONS
SESSION_ENGINE = env("SESSION_ENGINE", default='django.contrib.sessions.backends.cache')

# EMAIL
EMAIL_BACKEND=env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_TIMEOUT = env("EMAIL_TIMEOUT", default=5)
EMAIL_HOST= env('EMAIL_HOST', default="smtp.gmail.com")
EMAIL_USE_TLS= env.bool('EMAIL_USE_TLS', default=True)
EMAIL_PORT = env("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")


# IF POST_OFFICE BEING USED
POST_OFFICE = {
    'DEFAULT_PRIORITY' : 'now'
}

# ADMIN
ADMIN_URL = "admin/"
ADMINS = [("Mark Bronstein", "mark@bronsteinlaw.com")]
MANAGERS = ADMINS


# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_FILTER_BACKENDS": ['django_filters.rest_framework.DjangoFilterBackend'],
}

# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
CORS_URLS_REGEX = r"^/api/.*$"
# Your stuff...
# ------------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# settings for django-phonenumber_field
PHONENUMBER_DEFAULT_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'US'

#settings for django-import-export
IMPORT_EXPORT_USE_TRANSACTIONS=True

PDFTK_PATH = env('PDFTK_PATH')

# ------------------------------------------------------------------------------
SHELL_PLUS_POST_IMPORTS = (
    ('ssoffices.api.serializers', '*'),
    ('ssoffices.api.views', '*')
)

#PROFILER
SILK = env.bool("SILK")

if SILK is True:
    INSTALLED_APPS += ["silk"]
    MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]


DEBUG = env.bool("DEBUG")

DEBUG_TOOLBAR = env.bool("DEBUG_TOOLBAR")
if DEBUG_TOOLBAR is True:
    INSTALLED_APPS += ["debug_toolbar"]
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
    INTERNAL_IPS = env("INTERNAL_IPS").split(",")

    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
    }


