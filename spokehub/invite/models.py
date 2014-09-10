from django.db import models
from django.core.mail import send_mail


class Invite(models.Model):
    email = models.TextField()
    token = models.TextField()
    status = models.TextField(default='OPEN')
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def send_invite(self):
        send_mail(
            'You are invited to join Spokehub',
            """Hello,

You have been invited to join Spokehub.org. To sign up,
go here:

    http://spokehub.org/invite/signup/%s/

-Spokehub staff""" % self.token,
            'hello@spokehub.org',
            [self.email],
            fail_silently=False
            )
