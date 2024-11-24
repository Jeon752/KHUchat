from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('create/', views.create_chat_room, name='create_chat_room'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('load_messages/<str:room_name>/', views.load_messages, name='load_messages'),
]