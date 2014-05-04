# flake8: noqa
from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/spokehub/spokehub/spokehub/templates",
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

COMPRESS_ROOT = "/var/www/spokehub/spokehub/media/"
DEBUG = False
TEMPLATE_DEBUG = DEBUG

STATSD_PATCHES = ['django_statsd.patches.db', ]
if 'migrate' not in sys.argv:
    INSTALLED_APPS = INSTALLED_APPS + [
        'raven.contrib.django.raven_compat',
    ]


try:
    from local_settings import *
except ImportError:
    pass
