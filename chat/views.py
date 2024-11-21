from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ChatRoom, Message
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def create_chat_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if not room_name:
            return HttpResponse("Room name is required.", status=400)

        room, created = ChatRoom.objects.get_or_create(name=room_name)
        if created:
            print(f"ChatRoom '{room_name}' created successfully.")
        else:
            print(f"ChatRoom '{room_name}' already exists.")

        return redirect('accounts:home')

    return render(request, 'chat/create_chat_room.html')


@login_required
def room(request, room_name):
    room, created = ChatRoom.objects.get_or_create(name=room_name)
    return render(request, 'chat/room.html', {'room_name': room.name})


def load_messages(request, room_name):
    messages = Message.objects.filter(room__name=room_name).order_by('timestamp')
    message_list = [
        {"username": msg.sender.username, "content": msg.content, "timestamp": msg.timestamp}
        for msg in messages
    ]
    return JsonResponse({"messages": message_list})
