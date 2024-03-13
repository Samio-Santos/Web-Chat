from django.contrib import admin
from .models import Profile, Message, Conversation


admin.site.register(Message)
admin.site.register(Profile)
admin.site.register(Conversation)