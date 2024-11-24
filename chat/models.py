from django.db import models
from django.conf import settings  # settings.AUTH_USER_MODEL 사용

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,  # auth.User 대신 settings.AUTH_USER_MODEL 사용
        related_name='chat_rooms',
        blank=True
    )

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"