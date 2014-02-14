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
STAGING_ENV = True

STATSD_PREFIX = 'spokehub-staging'
SENTRY_SITE = 'spokehub-staging'
SENTRY_SERVERS = ['http://sentry.ccnmtl.columbia.edu/sentry/store/']

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django')

    import logging
    from raven.contrib.django.handlers import SentryHandler
    logger = logging.getLogger()
    # ensure we havent already registered the handler
    if SentryHandler not in map(type, logger.handlers):
        logger.addHandler(SentryHandler())
        logger = logging.getLogger('sentry.errors')
        logger.propagate = False
        logger.addHandler(logging.StreamHandler())

try:
    from local_settings import *
except ImportError:
    pass
