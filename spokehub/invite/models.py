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
            """Dear Awesome Person,

This is an invitation to join the thinkers, makers and code-breakers at
spokehub.org

Here is your unique sign up link:

http://spokehub.org/invite/signup/%s/

There are only 3 rules:
1. Shoot any feedback to hello@spokehub.org (that's why you've been invited
first!).
2. Share dreams not creds. We like how you think (that's why you're
invited).
3. Connect don't compete. This is a unicorn party (that's why you're
invited).

We look forward to seeing you in the hub.

            """ % self.token,
            'hello@spokehub.org',
            [self.email],
            fail_silently=False
            )
