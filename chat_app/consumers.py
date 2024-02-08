from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import ProfileUser
from chat_app.models import Message, Conversation
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from notifications.models import Notification
from decode import save_base64_image
import json
import secrets

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Obtém o nome da sala da URL
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        # Recupere o usuário logado usando a função get_user_from_scope
        scope_user = await self.get_user_from_scope(self.scope)

        # Autentique o usuário com base no token
        self.user = await self.get_user_from_token(self.room_name)

        self.token_channel = await self.get_user_token_channel(self.user, scope_user)

        if self.user:
            # Gera um canal único para o usuário
            self.user_channel_name = self.token_channel

            # Adiciona o usuário ao grupo
            await self.channel_layer.group_add(
                self.user_channel_name,
                self.channel_name
            )


            await self.accept()
        else:
            # Feche a conexão se o usuário não for autenticado
            await self.close()

    async def disconnect(self, close_code):
            # Remove o usuário do grupo ao desconectar
            await self.channel_layer.group_discard(
                self.user_channel_name,
                self.channel_name
            )

    @database_sync_to_async
    def get_user_from_scope(self, scope):
        # Obtenha o usuário do escopo
        return scope["user"]

    @database_sync_to_async
    def get_receiver(self, receiver_id):
        try:
            # Obtém o perfil do usuário receptor com base no username
            return ProfileUser.objects.get(token=receiver_id)
        except ProfileUser.DoesNotExist:
            raise ValueError(f"Receiver user with id {receiver_id} not found")

    @database_sync_to_async
    def get_sender_profile(self, sender):
        if isinstance(sender, User):
            # Obtém o perfil do usuário remetente com base no usuário do Django
            return ProfileUser.objects.get(user_ptr=sender)
        elif isinstance(sender, ProfileUser):
            # Se o remetente já for um ProfileUser, retorna o próprio perfil
            return sender
        else:
            raise ValueError(f"Invalid sender type: {type(sender)}")
        
    @database_sync_to_async
    def get_count_notification(self, receiver):

        count = Notification.objects.unread().filter(recipient=receiver).count()

        count += 1

        return count

    @database_sync_to_async
    def save_message(self, sender, receiver, message="", media_data=None):
        data = {}

        cv = Conversation.objects.filter(Q(owner=sender, user1=sender, user2=receiver)).first()

        # verifica se existe pelo menos uma mensagem entre  os dois usuários
        data['existMessage'] = Message.objects.filter(Q(conversation=cv) and Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)).exists()


        cv.notification = Notification.objects.create(actor=sender, 
        recipient=receiver, verb=f"você recebeu uma mensagem de {sender}")
        cv.save()

        # Cria uma nova mensagem
        msg = Message()

        media_path = media_data.get('mediaPath')

        if media_path is not None:
            mime_type = media_data['type']
            subtype = mime_type.split("/")


            if subtype[0].capitalize() == "Image":
                file = save_base64_image(sender.username, mime_type ,media_path)
                msg.media = file
                data['media'] = msg.media.url


            elif subtype[0].capitalize() == "Video":
                file = save_base64_image(sender.username, mime_type ,media_path)
                msg.video = file
                data['video'] = msg.video.url

            
            elif subtype[0].capitalize() == "Application":
                file = save_base64_image(sender.username, mime_type ,media_path)
                msg.pdf = file
                data['pdf'] = msg.pdf.url

        msg.conversation = cv
        msg.sender = sender
        msg.receiver = receiver
        msg.content = message
        msg.save()

        return data


    async def receive(self, text_data):
        try:
            # Converte os dados recebidos em formato JSON
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message")
            receiver_id = self.room_name


            # Obtém o usuário remetente da conexão WebSocket
            sender = self.scope["user"]

            # Obtém os perfis do remetente e do destinatário
            sender_profile = await self.get_sender_profile(sender)
            receiver = await self.get_receiver(receiver_id)

            to_user  = await self.get_user_from_token(receiver_id)

            
            if to_user:
                count = await self.get_count_notification(receiver)

                # Salva a mensagem no banco de dados (lógica a ser implementada)
                file_user = await self.save_message(sender_profile, receiver, message, text_data_json)


                # Use timezone.now() para obter o horário atual do servidor
                timestamp = timezone.now().strftime("%d de %B de %Y às %H:%M")

                # Envia a mensagem ou a mídia para o grupo da sala
                await self.channel_layer.group_send(
                    self.token_channel, {
                        "type": "chat.message",
                        "message": message if message is not None else "",
                        "sender": sender_profile.username,
                        "sender_img": sender_profile.imagem.url,
                        "sender_token": sender_profile.token,

                        "receiver": receiver_id,
                        "receiver_name": receiver.username,
                        "receiver_img": receiver.imagem.url,

                        "count_notification": count,

                        "existMessage": file_user.get('existMessage', ''),

                        "img_file": file_user.get('media', ''),

                        "pdf": file_user.get('pdf', ''),

                        "video": file_user.get('video', ''),

                        "timestamp": timestamp
                    }
                )


        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            await self.send_error("Invalid JSON format")
        except ValueError as e:
            print(f"Error processing message: {e}")
            await self.send_error(str(e))
        except Exception as e:
            print(f"Error: {e}")
            await self.send_error("An unexpected error occurred.")

    async def chat_message(self, event):

            # Envia a mensagem ou a mídia de volta para a conexão WebSocket
            await self.send(text_data=json.dumps(event))
    
    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            profile = ProfileUser.objects.get(token=token)

            return profile
        
        except ProfileUser.DoesNotExist:
            return None
        
  
    @database_sync_to_async
    def get_user_token_channel(self, user1, user2):
        try:
            # Tenta encontrar uma conversa existente
            conversation = Conversation.objects.get(Q(owner=user1, user1=user1, user2=user2))

            token_channel = conversation.token_channel
        except Conversation.DoesNotExist:
            # Se a conversa não existe, cria uma nova
            token_channel = secrets.token_urlsafe(5)

            conversation = Conversation.objects.create(owner=user1, user1=user1, user2=user2, token_channel=token_channel)

            conversatio = Conversation.objects.create(owner=user2, user1=user2, user2=user1, token_channel=token_channel)
        except Exception as e:
            print(f"Erro ao recuperar o canal do usuário {user1.username}: {e}")
            return None

        return token_channel

    
    async def send_error(self, error_message):
        # Envia mensagens de erro para a conexão WebSocket
        await self.send(text_data=json.dumps({
            "error": error_message,
        }))

