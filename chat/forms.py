from django import forms
from .models import ChatRoom

class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name']  # 사용자가 입력할 필드
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter chat room name'}),
        }