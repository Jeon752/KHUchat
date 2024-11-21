from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=200)  # 공모전 제목
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)  # 공모전 사진 (선택)
    content = models.TextField()  # 공모전 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 날짜
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 작성자
    is_admin_post = models.BooleanField(default=False)  # 관리자 작성 여부
    

    def save(self, *args, **kwargs):
        # 작성자가 관리자인 경우 is_admin_post를 True로 설정
        self.is_admin_post = self.author.is_staff
        super().save(*args, **kwargs)
       
    def __str__(self):
        return self.title
