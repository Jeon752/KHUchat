from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from .models import CustomUser
from chat.models import ChatRoom
from django.urls import reverse



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # 사용자 저장
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
    user = CustomUser.objects.get(username=username)
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user != user:
        return redirect('home')
    return render(request, 'accounts/profile.html', {'profile_user': user})

def home(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    chat_rooms = ChatRoom.objects.filter(participants=request.user)
    return render(request, 'accounts/home.html', {'chat_rooms': chat_rooms})