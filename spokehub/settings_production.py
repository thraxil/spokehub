# flake8: noqa
from settings_shared import *
import os.path

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

MEDIA_ROOT = '/var/www/spokehub/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/spokehub/spokehub/sitemedia'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'spokehub',
        'HOST': '',
        'PORT': 6432,
        'USER': '',
        'PASSWORD': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'spokehub-snowflake',
    }
}

COMPRESS_OFFLINE = True
COMPRESS_ENABLED = True
COMPRESS_ROOT = os.path.join(os.path.dirname(__file__), "../media")
DEBUG = False
TEMPLATE_DEBUG = DEBUG

STATSD_PATCHES = ['django_statsd.patches.db', ]

TWITTER_USER = 'spokehubNOW'
INSTAGRAM_USER = 'spokehubnow'

NOW_POSTS_PER_PAGE = 500

INSTALLED_APPS += [
    'opbeat.contrib.django',
]
MIDDLEWARE_CLASSES.insert(0, 'opbeat.contrib.django.middleware.OpbeatAPMMiddleware')

try:
    from local_settings import *
except ImportError:
    pass
