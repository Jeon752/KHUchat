from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']  # 필요한 필드만 포함

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # 사용자 정보를 폼에 전달
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        post = super().save(commit=False)
        if self.user:
            post.author = self.user  # 폼에 전달된 사용자 설정
        if commit:
            post.save()
        return post