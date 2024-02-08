from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .models import Profile, Message, Conversation

admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Conversation)