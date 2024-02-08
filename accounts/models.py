from django.db import models
from django.contrib.auth.models import AbstractUser
import secrets
import os


def user_profile_image_path(instance, filename):
    # Gera um token único
    token = secrets.token_urlsafe(32)
    # Obtém a extensão do arquivo original
    _, ext = os.path.splitext(filename)
    # Formata o nome do arquivo como 'token.ext'
    new_filename = f"{token}{ext}"
    # Retorna o caminho completo incluindo a pasta do usuário
    return os.path.join('foto_perfil', instance.username, new_filename)

class ProfileUser(AbstractUser):
    sexo = models.CharField(max_length=15, blank=True, null=True, default=None)
    biografia = models.TextField(blank=True)
    imagem = models.ImageField(blank=True, upload_to=user_profile_image_path)
    is_online = models.BooleanField(default=False)
    token = models.CharField(max_length=255, blank=True, null=True, unique=True)


