from django.contrib import admin
from .models import ChatRoom

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # 관리자 페이지에서 표시할 필드