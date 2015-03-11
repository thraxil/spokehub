from django.contrib import admin
from .models import Item, Reply, NowPost

admin.site.register(Item)
admin.site.register(Reply)
admin.site.register(NowPost)
