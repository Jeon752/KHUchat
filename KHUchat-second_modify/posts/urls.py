from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post_list'),  # 목록
    path('create/', views.post_create, name='post_create'),  # 글쓰기
    path('<int:post_id>/', views.post_detail, name='post_detail'),  # 상세보기
]
