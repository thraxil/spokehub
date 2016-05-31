from django.db import models
from django.core.mail import send_mail


class Invite(models.Model):
    email = models.TextField()
    token = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Invite to %s [%s]" % (self.email, str(self.added))

    def send_invite(self):
        send_mail(
            'Your invitation to join SPOKEHUB.',
            """"How We Work Now" is more than a tagline.

We are thinkers and makers - experts across disciplines - individual
but connected.

We are a disruptive design network - bringing independent experts
together for projects driving progress.

SPOKEHUB members share inspiration, dialogue, partnership,
opportunities and briefs from around the world.

We like how you work. Won't you join us?

http://spokehub.org/invite/signup/%s/
            """ % self.token,
            'Hub Conversation <hello@spokehub.org>',
            [self.email],
            fail_silently=False
            )
