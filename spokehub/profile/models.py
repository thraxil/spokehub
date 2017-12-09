from django.db import models
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from easy_thumbnails.fields import ThumbnailerImageField


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
