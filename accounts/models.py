from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)  # 자기소개 필드
    programming_languages = models.ManyToManyField('ProgrammingLanguage', blank=True)  # 여러 개의 프로그래밍 언어 선택

    def __str__(self):
        return self.username

class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name