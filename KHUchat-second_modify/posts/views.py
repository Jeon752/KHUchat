from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def post_list(request):
    sort_by = request.GET.get('sort_by', 'created_at')  # 기본 정렬 기준
    posts = Post.objects.all().order_by(f'-{sort_by}')
    return render(request, 'posts/post_list.html', {'posts': posts, 'sort_by': sort_by})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # `user` 전달 제거
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 현재 사용자를 작성자로 설정
            post.save()
            return redirect('posts:post_list')
    else:
        form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("이 글에 접근할 권한이 없습니다.")
    return render(request, 'posts/post_detail.html', {'post': post})




