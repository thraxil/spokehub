from django.core.mail import send_mail
from django.db import models
from django.template import Context
from django.template.loader import get_template


class Invite(models.Model):
    email = models.TextField()
    token = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Invite to %s [%s]" % (self.email, str(self.added))

    def send_invite(self):
        plaintext = get_template('email/invite.txt')
        d = Context({'token': self.token})
        text_content = plaintext.render(d)
        send_mail(
            'Your invitation to join SPOKEHUB.',
            text_content,
            'Hub Conversation <hello@spokehub.org>',
            [self.email],
            fail_silently=False
            )
