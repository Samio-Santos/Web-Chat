from django.db import models
from accounts.models import ProfileUser
from notifications.models import Notification

class Profile(models.Model):
    user = models.OneToOneField(ProfileUser, on_delete=models.CASCADE)


class Conversation(models.Model):
    owner = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name="owned_conversations")
    user1 = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name="user1_conversations")
    user2 = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name="user2_conversations")
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, null=True, blank=True)
    token_channel = models.CharField(max_length=255, blank=True, null=True, unique=False)
    is_active = models.BooleanField(default=True)
    archive = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.user1.username} -- {self.user2.username}'


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField(null=True, blank=True)
    media = models.ImageField(upload_to='media/', null=True, blank=True)
    pdf = models.FileField(upload_to='media/', null=True, blank=True)
    video = models.FileField(upload_to='media/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"sender: {self.sender.username} receiver: {self.receiver.username}"



