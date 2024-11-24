import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth.models import AnonymousUser
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 고정된 메인 채팅방 이름 사용
        self.room_name = "main"
        self.room_group_name = f'chat_{self.room_name}'

        # 그룹에 참가
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # 그룹에서 나가기
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = (
            self.scope['user'].username
            if self.scope['user'].is_authenticated
            else "Guest"
        )

        # Save the message to the database
        await self.save_message(username, message)

        # 그룹에 메시지 전송
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        # WebSocket으로 메시지 전송
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))

    @sync_to_async
    def save_message(self, username, message):
        # 데이터베이스에 메시지 저장
        Message.objects.create(
            sender=self.scope['user'] if self.scope['user'].is_authenticated else None,
            content=message,
        )