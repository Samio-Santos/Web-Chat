import uuid
import os
import base64
from django.conf import settings

from django import setup

# Defina a variável de ambiente DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_app.settings")

# Carregue as configurações do Django
setup()


def save_base64_image(base64_string, media_root=settings.MEDIA_ROOT):
    try:
        # Decodifica a string base64
        image_data = base64.b64decode(base64_string)

        # Gera um nome de arquivo aleatório (você pode usar sua própria lógica)
        filename = f"{uuid.uuid4().hex}.jpg"

        # Caminho completo para o arquivo no diretório MEDIA_ROOT
        filepath = os.path.join(media_root, filename)

        # Salva a imagem no disco
        with open(filepath, 'wb') as f:
            f.write(image_data)

        return filename  # ou filepath, dependendo do que você precisa
    except Exception as e:
        print(f"Erro ao salvar imagem: {e}")
        return None



