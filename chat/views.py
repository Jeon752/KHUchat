from django.shortcuts import render, redirect, get_object_or_404
from .models import ChatRoom, Message
from .forms import ChatRoomForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

# 채팅방 생성
@login_required
def create_chat_room(request):
    if request.method == 'POST':
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            chat_room = form.save(commit=False)
            chat_room.save()
            chat_room.participants.add(request.user)  # 방을 만든 사용자를 참가자로 추가
            return redirect('chat:room_list')  # 채팅방 목록 페이지로 리디렉션
    else:
        form = ChatRoomForm()
    return render(request, 'chat/create_chat_room.html', {'form': form})

# 채팅방 목록
@login_required
def room_list(request):
    chat_rooms = ChatRoom.objects.all()
    return render(request, 'chat/room_list.html', {'chat_rooms': chat_rooms})

# 채팅방 상세 페이지 (room_id로 찾기)
@login_required
def room_detail(request, room_id):
    try:
        room = ChatRoom.objects.get(id=room_id)  # 채팅방 찾기
    except ChatRoom.DoesNotExist:
        return redirect('chat:room_list')  # 채팅방이 없으면 채팅방 목록으로 리디렉션

    # 방에 참여한 사용자를 추가
    room.participants.add(request.user)

    # 해당 채팅방에 있는 메시지들 가져오기
    messages = Message.objects.filter(room=room)

    return render(request, 'chat/room_detail.html', {'room': room, 'messages': messages})

# 채팅방 접속 (room_name으로 찾기)
@login_required
def room(request, room_name):
    room = get_object_or_404(ChatRoom, name=room_name)
    return render(request, 'chat/room.html', {'room': room})

# 메시지 보내기
@login_required
def send_message(request, room_id):
    if request.method == 'POST':
        room = ChatRoom.objects.get(id=room_id)
        content = request.POST.get('content')

        # 메시지 저장
        message = Message.objects.create(room=room, user=request.user, content=content)

        # 메시지 보내고, 다시 방 상세 페이지로 리디렉션
        return HttpResponseRedirect(reverse('chat:room_detail', args=[room.id]))

from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the home page!")
