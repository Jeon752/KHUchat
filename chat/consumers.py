import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message
from django.contrib.auth.models import User
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # 방에 참여
        self.room = await database_sync_to_async(ChatRoom.objects.get)(name=self.room_name)
        self.chat_room_group_name = f'chat_{self.room.name}'

        # WebSocket 연결 승인
        await self.accept()

    async def disconnect(self, close_code):
        # WebSocket 연결 종료 처리
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 메시지 저장
        new_message = Message.objects.create(room=self.room, user=self.scope['user'], content=message)

        # 채팅방에 메시지 전송
        await self.send(text_data=json.dumps({
            'message': message,
        }))