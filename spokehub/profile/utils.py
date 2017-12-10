from django.conf import settings
from django.utils.encoding import smart_bytes
from django.utils.http import urlencode
from django.utils.six import text_type
from hashlib import sha1, md5
from userena.compat import SiteProfileNotAvailable, get_model

import datetime
import random

DEFAULT_USERENA_USE_HTTPS = False
_USERENA_USE_HTTPS = getattr(settings, 'USERENA_USE_HTTPS',
                             DEFAULT_USERENA_USE_HTTPS)
USERENA_MUGSHOT_GRAVATAR_SECURE = getattr(settings,
                                          'USERENA_MUGSHOT_GRAVATAR_SECURE',
                                          _USERENA_USE_HTTPS)


def get_profile_model():
    """
    Return the model class for the currently-active user profile
    model, as defined by the ``AUTH_PROFILE_MODULE`` setting.
    :return: The model that is used as profile.
    """
    if (not hasattr(settings, 'AUTH_PROFILE_MODULE')) or \
       (not settings.AUTH_PROFILE_MODULE):
        raise SiteProfileNotAvailable

    try:
        profile_mod = get_model(*settings.AUTH_PROFILE_MODULE.rsplit('.', 1))
    except LookupError:
        profile_mod = None

    if profile_mod is None:
        raise SiteProfileNotAvailable
    return profile_mod


def get_user_profile(user):
    profile_model = get_profile_model()
    try:
        profile = user.get_profile()
    except AttributeError:
        related_name = profile_model._meta.get_field('user')\
                                    .related_query_name()
        profile = getattr(user, related_name, None)
    except profile_model.DoesNotExist:
        profile = None
    if profile:
        return profile
    return profile_model.objects.create(user=user)


def get_gravatar(email, size=80, default='identicon'):
    if USERENA_MUGSHOT_GRAVATAR_SECURE:
        base_url = 'https://secure.gravatar.com/avatar/'
    else:
        base_url = '//www.gravatar.com/avatar/'

    gravatar_url = ('%(base_url)s%(gravatar_id)s?' %
                    {
                        'base_url': base_url,
                        'gravatar_id': md5(
                            email.lower().encode(
                                'utf-8')).hexdigest()})

    gravatar_url += urlencode({
        's': str(size),
        'd': default
    })
    return gravatar_url


def generate_sha1(string, salt=None):
    if not isinstance(string, (str, text_type)):
        string = str(string)

    if not salt:
        salt = sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]

    salted_bytes = (smart_bytes(salt) + smart_bytes(string))
    hash_ = sha1(salted_bytes).hexdigest()

    return salt, hash_


def get_datetime_now():
    """
    Returns datetime object with current point in time.
    In Django 1.4+ it uses Django's django.utils.timezone.now() which returns
    an aware or naive datetime that represents the current point in time
    when ``USE_TZ`` in project's settings is True or False respectively.
    In older versions of Django it uses datetime.datetime.now().
    """
    try:
        from django.utils import timezone
        return timezone.now()
    except ImportError:
        return datetime.datetime.now()
