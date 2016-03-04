from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from easy_thumbnails.fields import ThumbnailerImageField


class Profile(UserenaBaseProfile):
    user = models.OneToOneField(
        User,
        unique=True,
        verbose_name=_('user'),
        related_name='profile')
    about_me = models.TextField(blank=True, default="")
    profession = models.CharField(max_length=256, blank=True, default="")
    website_url = models.CharField(max_length=256, blank=True, default="")
    website_name = models.CharField(max_length=256, blank=True, default="")
    location = models.CharField(max_length=256, blank=True, default="")
    cover = ThumbnailerImageField('cover', blank=True, upload_to='covers')

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
