import json
import hashlib  # 해시를 위한 라이브러리
import urllib.parse
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message
from django.contrib.auth.models import AnonymousUser
from django.db import connection
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # URL에서 room_name을 디코딩
        encoded_room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_name = urllib.parse.unquote(encoded_room_name)

        # Group name 규칙을 준수하기 위해 SHA256 해시 사용
        hash_object = hashlib.sha256(self.room_name.encode('utf-8'))
        safe_room_name = hash_object.hexdigest()[:50]  # 해시 값을 잘라서 사용
        self.room_group_name = f'chat_{safe_room_name}'  # ASCII-safe 그룹 이름 생성
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = self.scope['user'].username if self.scope['user'].is_authenticated else "Guest"

        # Save the message to the database
        await self.save_message(username, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))

    @sync_to_async
    def save_message(self, username, message):
        # Fetch the chat room
        room, created = ChatRoom.objects.get_or_create(name=self.room_name)
        # Save the message
        Message.objects.create(
            room=room,
            sender=self.scope['user'] if self.scope['user'].is_authenticated else None,
            content=message,
        )
