from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/chat/$', consumers.ChatConsumer.as_asgi()),  # 고정된 메인 채팅방 경로
]