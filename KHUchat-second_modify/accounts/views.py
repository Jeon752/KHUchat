from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_backends  # get_backends 추가(2024-11-19 18:24 전준하)
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from .models import CustomUser
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from .utils import send_activation_email
from django.core.signing import BadSignature
from .utils import signer
from django.contrib.auth import get_user_model



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

    # 메인 채팅방 링크만 표시
    return render(request, 'accounts/home.html', {'user': request.user})

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', username=request.user.username)  # 네임스페이스 추가
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # 계정을 비활성화 상태로 저장
            user.save()
            send_activation_email(user)  # 이메일 인증 링크 전송
            messages.success(request, "회원가입이 완료되었습니다! 이메일을 확인해 인증을 완료해주세요.")
            return redirect('accounts:login')
        else:
            print("폼 검증 실패:", form.errors)  # 폼 검증 실패 원인 출력
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})





def activate_account(request, token):
    try:
        email = signer.unsign(token)  # 이메일 복호화 및 검증
        User = get_user_model()  # 현재 설정된 사용자 모델 가져오기
        user = User.objects.get(email=email)  # 이메일로 사용자 조회
        if user.is_active:
            messages.info(request, "이미 활성화된 계정입니다.")
        else:
            user.is_active = True  # 계정 활성화
            user.save()
            messages.success(request, "계정이 활성화되었습니다! 이제 로그인하실 수 있습니다.")
    except (User.DoesNotExist, BadSignature):
        messages.error(request, "유효하지 않은 링크입니다.")
    return redirect('accounts:login')  # 로그인 페이지로 리다이렉트


def logout_view(request):
    logout(request)
    return redirect(reverse('accounts:login'))  # 앱 이름을 포함해 정확히 지정
