from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.room, name='room'),  # Main chat room
    path('load_messages/', views.load_messages, name='load_messages'),  # Fixed load messages endpoint
]