from django.conf import settings

from userena.compat import SiteProfileNotAvailable, get_model


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
