from django.contrib import admin
from .models import Conversation, Reply, NowPost

admin.site.register(Conversation)
admin.site.register(Reply)
admin.site.register(NowPost)
