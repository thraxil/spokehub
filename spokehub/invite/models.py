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
            'Invitation to SPOKEHUB',
            """Here's your unique invitation link to join the hub online:

http://spokehub.org/invite/signup/%s/

As a logged in member you can make and respond to requests for visual
exploration (on the WE page)  with all activity hyperlinked to your own
professional website.

You can also share news and works in progress (on the NOW page) by
hash-tagging #spokehubnow on your social media posts.

Please shoot a message to hello@spokehub.org if you find any glitches!

Thanks & see you in the hub.
            """ % self.token,
            'Hub Conversation <hello@spokehub.org>',
            [self.email],
            fail_silently=False
            )
