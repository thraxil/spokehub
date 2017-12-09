from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import get_template
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from guardian.shortcuts import get_perms
from easy_thumbnails.fields import ThumbnailerImageField
from userena.mail import UserenaConfirmationMail
from userena.managers import UserenaBaseProfileManager, UserenaManager
from userena.utils import (get_datetime_now,
                           user_model_label, get_protocol)
from .utils import get_gravatar, generate_sha1


USERENA_MUGSHOT_SIZE = getattr(settings,
                               'USERENA_MUGSHOT_SIZE',
                               80)
USERENA_MUGSHOT_CROP_TYPE = getattr(settings,
                                    'USERENA_MUGSHOT_CROP_TYPE',
                                    'smart')
USERENA_WITHOUT_USERNAMES = getattr(settings,
                                    'USERENA_WITHOUT_USERNAMES',
                                    False)
USERENA_MUGSHOT_GRAVATAR = getattr(settings,
                                   'USERENA_MUGSHOT_GRAVATAR',
                                   True)
USERENA_MUGSHOT_DEFAULT = getattr(settings,
                                  'USERENA_MUGSHOT_DEFAULT',
                                  'identicon')
USERENA_DEFAULT_PRIVACY = getattr(settings,
                                  'USERENA_DEFAULT_PRIVACY',
                                  'registered')
USERENA_MUGSHOT_PATH = getattr(settings,
                               'USERENA_MUGSHOT_PATH',
                               'mugshots/')
PROFILE_PERMISSIONS = (
            ('view_profile', 'Can view profile'),
)


def upload_to_mugshot(instance, filename):
    """
    Uploads a mugshot for a user to the ``USERENA_MUGSHOT_PATH`` and
    saving it under unique hash for the image. This is for privacy
    reasons so others can't just browse through the mugshot directory.

    """
    extension = filename.split('.')[-1].lower()
    salt, hash = generate_sha1(instance.pk)
    path = USERENA_MUGSHOT_PATH % {
        'username': instance.user.username,
        'id': instance.user.id,
        'date': instance.user.date_joined,
        'date_now': get_datetime_now().date()}
    return '%(path)s%(hash)s.%(extension)s' % {'path': path,
                                               'hash': hash[:10],
                                               'extension': extension}


@python_2_unicode_compatible
class UserenaBaseProfile(models.Model):
    """ Base model needed for extra profile functionality """
    PRIVACY_CHOICES = (
        ('open', _('Open')),
        ('registered', _('Registered')),
        ('closed', _('Closed')),
    )

    MUGSHOT_SETTINGS = {'size': (USERENA_MUGSHOT_SIZE,
                                 USERENA_MUGSHOT_SIZE),
                        'crop': USERENA_MUGSHOT_CROP_TYPE}

    mugshot = ThumbnailerImageField(
        _('mugshot'),
        blank=True,
        upload_to=upload_to_mugshot,
        resize_source=MUGSHOT_SETTINGS,
        help_text=_('A personal image displayed in your profile.'))

    privacy = models.CharField(
        _('privacy'),
        max_length=15,
        choices=PRIVACY_CHOICES,
        default=USERENA_DEFAULT_PRIVACY,
        help_text=_('Designates who can view your profile.'))

    objects = UserenaBaseProfileManager()

    class Meta:
        abstract = True
        permissions = PROFILE_PERMISSIONS

    def __str__(self):
        return 'Profile of %(username)s' % {'username': self.user.username}

    def get_mugshot_url(self):
        # First check for a mugshot and if any return that.
        if self.mugshot:
            return self.mugshot.url

        # Use Gravatar if the user wants to.
        if USERENA_MUGSHOT_GRAVATAR:
            return get_gravatar(self.user.email,
                                USERENA_MUGSHOT_SIZE,
                                USERENA_MUGSHOT_DEFAULT)

        # Gravatar not used, check for a default image.
        else:
            if USERENA_MUGSHOT_DEFAULT not in ['404', 'mm',
                                               'identicon',
                                               'monsterid',
                                               'wavatar']:
                return USERENA_MUGSHOT_DEFAULT
            else:
                return None

    def get_full_name_or_username(self):
        user = self.user
        if user.first_name or user.last_name:
            # We will return this as translated string. Maybe there are some
            # countries that first display the last name.
            name = _("%(first_name)s %(last_name)s") % \
                {'first_name': user.first_name,
                 'last_name': user.last_name}
        else:
            # Fallback to the username if usernames are used
            if not USERENA_WITHOUT_USERNAMES:
                name = "%(username)s" % {'username': user.username}
            else:
                name = "%(email)s" % {'email': user.email}
        return name.strip()

    def can_view_profile(self, user):
        # Simple cases first, we don't want to waste CPU and DB hits.
        # Everyone.
        if self.privacy == 'open':
            return True
        # Registered users.
        elif self.privacy == 'registered' and isinstance(
                user, get_user_model()):
            return True

        # Checks done by guardian for owner and admins.
        elif 'view_profile' in get_perms(user, self):
            return True

        # Fallback to closed profile.
        return False


class Profile(UserenaBaseProfile):
    user = models.OneToOneField(
        User,
        unique=True,
        verbose_name=_('user'),
        related_name='profile',
        on_delete=models.CASCADE)
    about_me = models.TextField(blank=True, default="")
    profession = models.CharField(max_length=256, blank=False)
    website_url = models.CharField(max_length=256, blank=False)
    website_name = models.CharField(max_length=256, blank=False)
    location = models.CharField(max_length=256, blank=False)
    cover = ThumbnailerImageField('Your background image', blank=True,
                                  upload_to='covers')
    allow_email = models.BooleanField(default=False,
                                      verbose_name='Allow Notifications')

    def completed(self):
        return (
            self.profession != "" and
            self.location != "" and
            self.user.first_name != "" and
            self.user.last_name != ""
        )

    def questions(self):
        return self.user.conversation_set.all()

    def replies(self):
        return self.user.reply_set.all()

    def replied_to(self):
        """ questions the user has replied to (other than ones they asked) """
        asked = set(self.questions())
        replies = set([r.item for r in self.replies()])
        replied_to = reversed(sorted(list(replies - asked),
                                     key=lambda x: x.added))
        return replied_to

    def hover_div(self):
        t = get_template('userena/hover_div.html')
        d = {'profile': self}
        return t.render(d)


@python_2_unicode_compatible
class UserenaSignup(models.Model):
    """
    Userena model which stores all the necessary information to have a full
    functional user implementation on your Django website.
    """
    user = models.OneToOneField(
        user_model_label,
        verbose_name=_('user'),
        related_name='userena_signup',
        on_delete=models.CASCADE)

    last_active = models.DateTimeField(
        _('last active'),
        blank=True,
        null=True,
        help_text=_('The last date that the user was active.'))

    activation_key = models.CharField(
        _('activation key'),
        max_length=40,
        blank=True)

    activation_notification_send = models.BooleanField(
        _('notification send'),
        default=False,
        help_text=_('Designates whether this user has already got '
                    'a notification about activating their account.'))

    email_unconfirmed = models.EmailField(
        _('unconfirmed email address'),
        blank=True,
        help_text=_('Temporary email address when the user '
                    'requests an email change.'))

    email_confirmation_key = models.CharField(
        _('unconfirmed email verification key'),
        max_length=40,
        blank=True)

    email_confirmation_key_created = models.DateTimeField(
        _('creation date of email confirmation key'),
        blank=True,
        null=True)

    objects = UserenaManager()

    class Meta:
        verbose_name = _('userena registration')
        verbose_name_plural = _('userena registrations')

    def __str__(self):
        return '%s' % self.user.username

    def change_email(self, email):
        self.email_unconfirmed = email

        salt, hash = generate_sha1(self.user.username)
        self.email_confirmation_key = hash
        self.email_confirmation_key_created = get_datetime_now()
        self.save()

        # Send email for activation
        self.send_confirmation_email()

    def send_confirmation_email(self):
        context = {
            'user': self.user,
            'without_usernames': USERENA_WITHOUT_USERNAMES,
            'new_email': self.email_unconfirmed,
            'protocol': get_protocol(),
            'confirmation_key': self.email_confirmation_key,
            'site': Site.objects.get_current()}

        mailer = UserenaConfirmationMail(context=context)
        mailer.generate_mail("confirmation", "_old")

        if self.user.email:
            mailer.send_mail(self.user.email)

        mailer.generate_mail("confirmation", "_new")
        mailer.send_mail(self.email_unconfirmed)
