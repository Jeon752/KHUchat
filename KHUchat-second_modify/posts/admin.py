from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')  # 관리자 페이지에서 표시할 필드
    list_filter = ('created_at', 'author')  # 필터링 기준
    search_fields = ('title', 'content')  # 검색 가능 필드
