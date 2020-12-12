from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django import forms

from blog.models import Blog, ContentImage
from blog.forms import BlogForm, SignUpForm, ContentImageForm

import math


def blog_list(request):
    user = request.user
    if user.is_authenticated:
        blogs = Blog.objects.order_by('-published_at').all()
    else:
        blogs = Blog.objects.filter(is_public=True, published_at__lte=timezone.now()).order_by('-published_at').all()
    paginator = Paginator(blogs, per_page=5)

    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        blogs = paginator.page(1)
    for blog in blogs:
        blog.info_content()
    if blogs.number <= 5:
        blogs.pages = range(1, min(10, paginator.num_pages) + 1)
    elif blogs.number >= paginator.num_pages - 4:
        blogs.pages = range(max(1, paginator.num_pages - 9), paginator.num_pages + 1)
    else:
        blogs.pages = range(blogs.number - 5, blogs.number + 5)
    blogs.last = paginator.num_pages
    return TemplateResponse(request, 'blog/list.html', {'blogs': blogs})


def blog_detail(request, blog_id):
    user = request.user
    if user.is_authenticated:
        blog = get_object_or_404(Blog, id=blog_id)
    else:
        blog = get_object_or_404(Blog, id=blog_id, is_public=True, published_at__lte=timezone.now())
    blog.sort_content()
    return TemplateResponse(request, 'blog/detail.html', {'blog': blog})


@login_required
def blog_add(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.save()
            return redirect('detail', blog_id=blog.id)
    else:
        form = BlogForm()
    return TemplateResponse(request, 'blog/addBlog.html', {'form': form})


@login_required
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = SignUpForm()

    return TemplateResponse(request, 'blog/signup.html', {'form': form})


@login_required
def user_menu(request):
    return TemplateResponse(request, 'blog/userMenu.html', {})


@login_required
def edit(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    confirm = False
    if request.method == 'GET':
        form = BlogForm(instance=blog)
    else:
        form = BlogForm(request.POST, instance=blog)
        if 'confirmed' in request.POST:
            if request.POST['confirmed'] == 'はい':
                blog.delete()
                return redirect('text_list')
        elif 'delete' in request.POST:
            confirm = True
        else:
            if form.is_valid():
                form.save()
                return redirect('detail', blog_id=blog_id)

    return TemplateResponse(request, 'blog/edit.html', {'form': form,
                                                        'blog_id': blog_id,
                                                        'confirm': confirm,
                                                        })


@login_required
def blog_text_list(request):
    blogs = Blog.objects.order_by('-published_at').all()
    paginator = Paginator(blogs, per_page=30)

    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        blogs = paginator.page(1)

    if blogs.number <= 5:
        blogs.pages = range(1, min(10, paginator.num_pages) + 1)
    elif blogs.number >= paginator.num_pages - 4:
        blogs.pages = range(max(1, paginator.num_pages - 9), paginator.num_pages + 1)
    else:
        blogs.pages = range(blogs.number - 5, blogs.number + 5)
    blogs.last = paginator.num_pages
    return TemplateResponse(request, 'blog/text_list.html', {'blogs': blogs})


@login_required
def image_upload(request):
    if request.method == 'POST':
        form = ContentImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.save()
            return redirect('edit', blog_id=image.blog.id)
    else:
        form = ContentImageForm()
    return TemplateResponse(request, 'blog/addImage.html', {'form': form})
