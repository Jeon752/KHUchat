from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_backends  # get_backends 추가(2024-11-19 18:24 전준하)
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from .models import CustomUser
from chat.models import ChatRoom
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # 사용자 저장
            backend = get_backends()[0]  # (2024-11-19 18:24 전준하)
            user.backend = f'{backend.__module__}.{backend.__class__.__name__}' # (2024-11-19 18:24 전준하)
            login(request, user)  # 자동으로 로그인
            return redirect('accounts:profile', username=user.username)  # 프로필 페이지로 리디렉션
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect(reverse('accounts:login'))  # 앱 이름을 포함해 정확히 지정

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        # 로그인 후 해당 사용자의 프로필 페이지로 리디렉션
        return reverse('accounts:home')

def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)  # username 기반으로 검색
    return render(request, 'accounts/profile.html', {'profile_user': user})

def home(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    chat_rooms = ChatRoom.objects.all()  # 모든 채팅방 표시
    # chat_rooms = ChatRoom.objects.filter(participants=request.user)  # 현재 사용자 참여 채팅방만 표시 (옵션)

    return render(request, 'accounts/home.html', {'chat_rooms': chat_rooms, 'user': request.user})

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', username=request.user.username)  # 네임스페이스 추가
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})