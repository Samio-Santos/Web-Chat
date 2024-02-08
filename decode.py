import uuid
import base64
import os
from django.conf import settings
from django import setup

# Defina a variável de ambiente DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_app.settings")

# Carregue as configurações do Django
setup()
def save_base64_image(user, type, encoded_image, save_directory=settings.MEDIA_ROOT):

    print(save_directory)
    try:
        mime_type = type
        subtype = mime_type.split("/")

        user_directory = os.path.join(save_directory, user)

        # Crie o diretório do usuário se não existir
        if not os.path.exists(user_directory):
            os.makedirs(user_directory)

        # Remova a string de codificação do prefixo 'data:image/jpeg;base64,'
        _, encoded_data = encoded_image.split(',', 1)
        
        # Decodifique a string base64 para bytes
        decoded_data = base64.b64decode(encoded_data)

        if subtype[0].capitalize() == "Image":
            # Gere um nome de arquivo único usando uuid
            file_name = f"{uuid.uuid4()}.{subtype[1]}"

        elif subtype[0].capitalize() == "Video":
            # Gere um nome de arquivo único usando uuid
            file_name = f"{uuid.uuid4()}.{subtype[1]}"
        
        elif subtype[0].capitalize() == "Application":
            # Gere um nome de arquivo único usando uuid
            file_name = f"{uuid.uuid4()}.{subtype[1]}"
        
    
        # Combine o nome do arquivo com o diretório de salvamento
        save_path = os.path.join(save_directory, file_name)
        print(save_directory)

        
        # Salve os bytes decodificados em um arquivo
        with open(save_path, 'wb') as file:
            file.write(decoded_data)
        
        return file_name
    
    except Exception as e:
        print(f"Erro ao decodificar ou salvar a arquivos: {e}")
