from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),  # 회원가입 페이지
    path('login/', views.CustomLoginView.as_view(), name='login'),  # 로그인 페이지
    path('logout/', views.logout_view, name='logout'),  # 로그아웃 처리
    path('profile/<str:username>/', views.profile, name='profile'),  # 프로필 페이지 (username 필요)
    path('', views.home, name='home'),  # 홈 페이지
]