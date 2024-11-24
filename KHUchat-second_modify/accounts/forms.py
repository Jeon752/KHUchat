# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, ProgrammingLanguage


PROGRAMMING_LANGUAGES = [
    ('Python', 'Python'),
    ('Java', 'Java'),
    ('C', 'C'),
    ('C++', 'C++'),
    ('JavaScript', 'JavaScript'),
    ('Ruby', 'Ruby'),
    ('PHP', 'PHP'),
    ('Swift', 'Swift'),
    ('Kotlin', 'Kotlin'),
    ('Go', 'Go'),
    ('Rust', 'Rust'),
    ('Dart', 'Dart'),
    ('TypeScript', 'TypeScript'),
    ('Perl', 'Perl'),
    ('Scala', 'Scala'),
    ('Haskell', 'Haskell'),
    ('Lua', 'Lua'),
    ('R', 'R'),
    ('MATLAB', 'MATLAB'),
    ('Visual Basic', 'Visual Basic'),
    ('Objective-C', 'Objective-C'),
    ('Groovy', 'Groovy'),
    ('Shell', 'Shell'),
    ('Assembly', 'Assembly'),
    ('Fortran', 'Fortran'),
    ('COBOL', 'COBOL'),
    ('Ada', 'Ada'),
    ('Erlang', 'Erlang'),
    ('Elixir', 'Elixir'),
    ('Clojure', 'Clojure'),
    ('F#', 'F#'),
    ('Scheme', 'Scheme'),
    ('Prolog', 'Prolog'),
    ('VBScript', 'VBScript'),
    ('SQL', 'SQL'),
]


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(help_text="Only @khu.ac.kr emails are allowed.")
    programming_languages = forms.MultipleChoiceField(
        choices=PROGRAMMING_LANGUAGES,
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
    programming_languages = forms.ModelMultipleChoiceField(
        queryset=ProgrammingLanguage.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'programming_languages']