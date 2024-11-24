from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Message
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# 고정된 메인 채팅방 이름 정의
MAIN_ROOM_NAME = "main"

@login_required
def room(request):
    return render(request, 'chat/room.html', {'room_name': MAIN_ROOM_NAME})


def load_messages(request):
    messages = Message.objects.order_by('-timestamp')[:50]  # Load the latest 50 messages
    return JsonResponse({
        'messages': [
            {
                'sender': message.sender.username,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for message in messages
        ]
    })