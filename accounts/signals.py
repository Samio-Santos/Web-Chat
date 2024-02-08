# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_out
from accounts.models import ProfileUser
import secrets


@receiver(post_save, sender=get_user_model())
def user_logged_in_handler(sender, instance, **kwargs):
    get_user_model().objects.filter(pk=instance.pk).update(is_online=True)

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, **kwargs):
    if request.user.is_authenticated:
        get_user_model().objects.filter(username=request.user).update(is_online=False)

@receiver(post_save, sender=ProfileUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Gera um token único
        token = secrets.token_urlsafe(32)
        instance.token = token
        instance.save()