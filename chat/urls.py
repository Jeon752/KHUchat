from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.room_list, name='room_list'),  # 채팅방 목록
    path('create/', views.create_chat_room, name='create_chat_room'),  # 채팅방 생성
    path('<int:room_id>/', views.room_detail, name='room_detail'),  # 채팅방 상세 (room_id 기준)
    path('<int:room_id>/send/', views.send_message, name='send_message'),  # 메시지 보내기
    path('<str:room_name>/', views.room, name='room'),
    path('', views.home, name='home'),
]