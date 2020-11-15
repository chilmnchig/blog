from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from blog.models import Blog
from blog.forms import BlogForm


def blog_list(request):
    blogs = Blog.objects.filter(is_public=True, published_at__lte=timezone.now()).order_by('-published_at').all()
    return TemplateResponse(request, 'blog/list.html', {'blogs': blogs})


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, is_public=True, published_at__lte=timezone.now())
    return TemplateResponse(request, 'blog/detail.html', {'blog': blog})


def blog_add(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = BlogForm
    return TemplateResponse(request, 'blog/add.html', {'form': form})
