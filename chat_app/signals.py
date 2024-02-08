from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from .models import Message, Conversation

@receiver(post_save, sender=Message)
def duplicate_conversation(sender, instance, created, **kwargs):

    if created:
        # Desconecta o sinal para evitar recursão
        post_save.disconnect(duplicate_conversation, sender=Message)

        # Encontra ou cria a conversa
        conversation = Conversation.objects.filter(
            Q(owner=instance.receiver),
            Q(user1=instance.sender, user2=instance.receiver) | Q(user1=instance.receiver, user2=instance.sender)
        ).first()


        if not conversation:
            conversation = Conversation.objects.create(
                owner=instance.receiver,
                user1=instance.receiver,
                user2=instance.sender
            )

        # Cria uma cópia da mensagem para a conversa
        message = Message.objects.create(
            conversation=conversation,
            sender=instance.sender,
            receiver=instance.receiver,
            content=instance.content,
            media=instance.media,
            pdf=instance.pdf,
            video=instance.video

        )

        # Reconecta o sinal após a conclusão
        post_save.connect(duplicate_conversation, sender=Message)

