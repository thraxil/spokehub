# Django settings for spokehub project.
import os.path
import sys
import requests
import mimetypes


DEBUG = True

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'spokehub',
        'HOST': '',
        'PORT': 5432,
        'USER': '',
        'PASSWORD': '',
        'ATOMIC_REQUESTS': True,
    }
}

RETICULUM_UPLOAD = "https://reticulum.thraxil.org"
RETICULUM_PUBLIC = "https://d2f33fmhbh7cs9.cloudfront.net"


class ReticulumUploader(object):
    def upload(self, f):
        content_type = mimetypes.guess_type(f.name)[0]
        files = {'image': (f.name, f, content_type)}
        r = requests.post(RETICULUM_UPLOAD + "/", files=files, verify=False)
        return r.json()["hash"]


UPLOADER = ReticulumUploader()

if 'test' in sys.argv or 'jenkins' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
        }
    }
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )

    class DummyUploader(object):
        def upload(self, f):
            return "fakehash"

    UPLOADER = DummyUploader()


TEST_RUNNER = 'django.test.runner.DiscoverRunner'
TEST_OUTPUT_DIR = 'reports'

PROJECT_APPS = [
    'spokehub.main', 'spokehub.work', 'spokehub.edit',
]

TEST_PROJECT_APPS = [
    'spokehub.main', 'spokehub.work', 'spokehub.edit',
]

ALLOWED_HOSTS = ['localhost', 'spokehub.com', 'spokehub.org']

USE_TZ = True
TIME_ZONE = 'GMT'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = "/var/www/spokehub/uploads/"
MEDIA_URL = '/uploads/'
STATIC_URL = '/media/'
SECRET_KEY = 'J#m2{>xXxByAK:RDvyEtJQiH_{fF@<WIJNHd7!Q`q*G:@i'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [
            "/var/www/spokehub/templates/",
            os.path.join(os.path.dirname(__file__), "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'gacontext.ga_processor',
                'django.contrib.messages.context_processors.messages',
                'spokehub.contact.context.add_contact_form',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'waffle.middleware.WaffleMiddleware',
]

ROOT_URLCONF = 'spokehub.urls'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_markwhat',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.admin',
    'compressor',
    'django_statsd',
    'bootstrap3',
    'bootstrapform',
    'waffle',
    'discover_jenkins',
    'smoketest',
    'registration',
    'spokehub.main',
    'spokehub.profile',
    'spokehub.twitter',
    'spokehub.instagram',
    'spokehub.invite',
    'spokehub.work',
    'spokehub.edit',
    'gunicorn',
    'guardian',
    'easy_thumbnails',
    'spokehub.gravatar',
    'spokehub.broadcast',
    'flatblocks',
    'raven.contrib.django.raven_compat',
]

INTERNAL_IPS = ('127.0.0.1', )
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
)

STATSD_CLIENT = 'statsd.client'
STATSD_PREFIX = 'spokehub'
STATSD_HOST = '127.0.0.1'
STATSD_PORT = 8125

THUMBNAIL_SUBDIR = "thumbs"
EMAIL_SUBJECT_PREFIX = "[spokehub] "
EMAIL_HOST = 'localhost'
SERVER_EMAIL = "spokehub@spokehub.org"
DEFAULT_FROM_EMAIL = SERVER_EMAIL

STATIC_ROOT = os.path.join(os.path.dirname(__file__), "../media")
STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_URL = "/media/"
COMPRESS_ROOT = "media/"
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)
if 'test' in sys.argv or 'jenkins' in sys.argv:
    COMPRESS_PRECOMPILERS = []

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
LOGIN_REDIRECT_URL = "/"

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60 * 24 * 365 * 5
USERENA_REMEMBER_ME_DAYS = ('', 365 * 5)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)
ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'profile.Profile'

LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}

ACCOUNT_ACTIVATION_DAYS = 7
USERENA_MUGSHOT_SIZE = 200
USERENA_SIGNIN_REDIRECT_URL = '/'
USERENA_DEFAULT_PRIVACY = "open"
USERENA_ACTIVATION_REQUIRED = False

USERENA_REDIRECT_ON_SIGNOUT = '/'

HASHTAG = "#spokehubnow"

NOW_POSTS_PER_PAGE = 50
