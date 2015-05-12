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

COMPRESS_OFFLINE = True
COMPRESS_ROOT = os.path.join(os.path.dirname(__file__), "../media")
DEBUG = False
TEMPLATE_DEBUG = DEBUG

STATSD_PATCHES = ['django_statsd.patches.db', ]
if 'migrate' not in sys.argv:
    INSTALLED_APPS = INSTALLED_APPS + [
        'raven.contrib.django.raven_compat',
    ]

TWITTER_USER = 'spokehubNOW'

try:
    from local_settings import *
except ImportError:
    pass
