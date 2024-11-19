from django.db import models
from django.conf import settings  # settings.AUTH_USER_MODEL 사용

class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,  # User 대신 AUTH_USER_MODEL
        related_name='chat_rooms'
    )

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom,
        related_name='messages',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # User 대신 AUTH_USER_MODEL
        related_name='messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}'