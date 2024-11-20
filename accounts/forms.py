# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, ProgrammingLanguage

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(help_text="Only @khu.ac.kr emails are allowed.")
    programming_languages = forms.ModelMultipleChoiceField(
        queryset=ProgrammingLanguage.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'bio', 'programming_languages']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@khu.ac.kr'):
            raise forms.ValidationError("You must use a @khu.ac.kr email address.")
        return email
    

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'programming_languages']  # 수정 가능한 필드
        widgets = {
            'programming_languages': forms.CheckboxSelectMultiple(),  # 프로그래밍 언어 선택
        }