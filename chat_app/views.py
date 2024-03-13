from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from urllib.parse import urlparse
from django.contrib.auth.decorators import login_required

from .models import Message, Conversation
from accounts.models import ProfileUser
from django.db.models import Q
from notifications.models import Notification

def index(request, room_name):
    return render(request, "chat_app/room.html", {"room_name": room_name})

@login_required(redirect_field_name='#usu@rio$',login_url='login')
def room(request, token):
    # Dicionário para armazenar os dados que serão enviados para o template
    data = {}
    mark_all = request.GET.get('mark')
    # Lista para armazenar os dados de cada mensagem
    messages_data = []
  
    # Lista para armazenar as informações da última mensagem de cada conversa
    conversation_data = []
    
    # Obtém o usuário remetente (quem está logado)
    user_sender = ProfileUser.objects.get(username=request.user)
    
    # Obtém o destinatário da conversa
    receiver = get_object_or_404(ProfileUser, token=token)

    # logica para pesquisa de usuarios no chat
    users_profile = []
    for users in ProfileUser.objects.all():
        if users != request.user:
            users_profile.append({"name":users.username,"photo":users.imagem.url, "token": users.token})


    # Filtra as mensagens entre o remetente e o destinatário ordenadas pelo timestamp
    messages = Message.objects.filter(Q(conversation__owner=user_sender, conversation__is_active=True), Q(conversation__user1=user_sender, conversation__user2=receiver) | Q(conversation__user1=receiver, conversation__user2=user_sender)).order_by("timestamp")

    # Loop sobre as mensagens filtradas
    for message in messages:
        messages_data.append({
            "sender": message.sender.username,
            "sender_img": message.sender.imagem,
            "receiver": message.receiver.username,
            "receiver_img": message.receiver.imagem,
            "content": message.content,
            "media": message.media,
            "file": message.pdf,
            "video": message.video,
            "timestamp": message.timestamp,
            "is_read": message.is_read,
        })

  
    # conta as notificação do usuarios que não foram lindas
    count_notify = 0

    if mark_all:
        
    # Marca todas as mensagens como lidas
        cv = Conversation.objects.filter(Q(owner=receiver, user1=receiver, user2=user_sender)).first()

        msgUser = Message.objects.filter(Q(conversation=cv, sender=receiver))

        if msgUser:
            msgUser.update(is_read=True)

    # Marca todas as notificações do user como visualizadas
        Notification.objects.filter(Q(recipient=user_sender, actor_object_id=receiver.id)).update(unread=False)

   
    # Loop sobre todas as mensagens do remetente
    conversation_all_by = Conversation.objects.filter(Q(owner=user_sender, is_active=True))
    strUser= str(user_sender)

    for cv in conversation_all_by:

        if cv.user2.username != strUser:

            conversation_all_to = Conversation.objects.filter(Q(owner=user_sender, user1=user_sender, user2=cv.user2.id, is_active=True)).first()

            msgUser = Message.objects.filter(Q(conversation=conversation_all_to, sender=user_sender)).order_by('-timestamp').first()

            if msgUser:
                # conta quantas message o user logado no sistema recebeu de outro usuario especifico
                count_notify = Notification.objects.unread().filter(Q(recipient__username=user_sender, actor_object_id=cv.user2.id)).count()

                
                notification_recipient = msgUser.conversation.notification

                notify_username = notification_recipient if notification_recipient is None else msgUser.conversation.notification.recipient.username

                conversation_data.append({
                    "username_sender": msgUser.sender.username,
                    "photo_sender": msgUser.sender.imagem.url,
                    "token_sender": msgUser.sender.token,

                    "username": msgUser.receiver.username,
                    "photo": msgUser.receiver.imagem.url,
                    "token": msgUser.receiver.token,

                    "conversation": msgUser.conversation.archive,
                    "owner": msgUser.conversation.owner.username,
                    "count_notify": count_notify,
                    "notify": notify_username,

                    "token_channel": msgUser.conversation.token_channel,
                    "content": msgUser.content,
                    "timestamp": msgUser.timestamp,
                    "is_read": msgUser.is_read,
                })
  

    # Adiciona informações do destinatário ao dicionário de dados
    data['receiver'] = receiver.username
    data['receiver_imagem'] = receiver.imagem

    # contatos onlines
    contant_online = []
    users_online = ProfileUser.objects.filter(is_online=True)
    
    for contant in users_online:
        if contant != request.user:
            user = ProfileUser.objects.get(username=contant)

            contant_online.append({
            'username': user.username,
            'token': user.token,
            'photo': user.imagem
        })
            
    # Adiciona os dados ao dicionário principal
    data['messages_data'] = messages_data
    data['conversation_data'] = sorted(conversation_data, key=lambda x: x['timestamp'], reverse=True)
    data['users_profile'] = users_profile
    data['users_online'] = contant_online

    data['room_name'] = token


    # Renderiza o template com os dados
    return render(request, "chat_app/chat.html", data)


def delete_or_archive(request, token_user):
    delete_or_archive = request.POST.get("data")

    print(delete_or_archive)
    print(token_user)
    
    user = get_object_or_404(ProfileUser, username=request.user)
    receiver = get_object_or_404(ProfileUser, token=token_user)


    # Salva o caminho do usuário antes de desativar as conversas
    current_url = urlparse(request.build_absolute_uri()).hostname
    port = urlparse(request.build_absolute_uri()).port

    conversations_to_deactivate = Conversation.objects.filter(
        Q(owner=user),
        Q(user1=user, user2=receiver) | Q(user1=receiver, user2=user)
    )

    # Desative as conversas
    if delete_or_archive == "Delete":
        for conversation in conversations_to_deactivate:
            conversation.is_active = False
            conversation.save()

    # Ariquiva uma conversa
    elif delete_or_archive == "Archive":
        for conversation in conversations_to_deactivate:
            conversation.archive = True
            conversation.save()
    
    elif delete_or_archive == 'unarchive':
        for conversation in conversations_to_deactivate:
            conversation.archive = False
            conversation.save()


    # Redirecione para o caminho do usuário
    return redirect(f"http://{current_url}:{port}/chat/{user.token}/")



