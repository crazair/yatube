from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User
from .utils import get_page_context_with_paginator


def index(request):
    posts = Post.objects.select_related('group', 'author')
    page_obj = get_page_context_with_paginator(request, posts)

    context = {'page_obj': page_obj}
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = get_page_context_with_paginator(request, posts)

    context = {
        'page_obj': page_obj,
        'group': group,
    }

    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User.objects.select_related(),
                               username=username)
    posts = author.posts.all()
    post_count = posts.count()
    page_obj = get_page_context_with_paginator(request, posts)

    context = {
        'author': author,
        'page_obj': page_obj,
        'post_count': post_count,
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    posts_count = Post.objects.filter(author=post.author).count()

    context = {
        'post': post,
        'posts_count': posts_count,
    }

    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('posts:profile', request.user)

    context = {
        'form': form,
    }

    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)

    context = {
        'post': post,
        'form': form,
        'is_edit': True,
    }

    return render(request, 'posts/create_post.html', context)
