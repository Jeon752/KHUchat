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