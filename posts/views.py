from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')  # 모든 게시물 조회
    return render(request, 'posts/post_list.html', {'posts': posts})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_list')
    else:
        form = PostForm(user=request.user)
    return render(request, 'posts/post_create.html', {'form': form})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})




