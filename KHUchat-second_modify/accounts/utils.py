from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.core.signing import Signer

signer = Signer()

def send_activation_email(user):
    try:
        token = signer.sign(user.email)
        activation_url = settings.DOMAIN + reverse('accounts:activate', args=[token])
        message = f"""
        안녕하세요, {user.username}님!

        아래 링크를 클릭하여 계정을 활성화하세요:
        {activation_url}
        """
        send_mail(
            subject="계정 활성화 이메일",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        print(f"Activation email sent to {user.email}")
    except Exception as e:
        print(f"Error sending activation email: {e}")

