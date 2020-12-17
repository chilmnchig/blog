from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from blog.models import Blog, ContentImage
from blog.forms import BlogForm, SignUpForm, ContentImageForm
from blog.paginator import get_pagination, page_for_two


def blog_list(request):
    blogs = Blog.get_list(request)
    blogs, page_info = get_pagination(request, blogs, per_page=5)
    for blog in blogs:
        blog.info_content()  # 50字まで内容を表示する
    page = page_info[0]
    page_max = page_info[1]
    page_range = page_info[2]
    context = {'blogs': blogs, 'page': page, 'page_max': page_max,
               'page_range': page_range}
    return TemplateResponse(request, 'blog/list.html', context)


def blog_detail(request, blog_id):
    blog = Blog.get_detail(request, blog_id)
    return TemplateResponse(request, 'blog/detail.html', {'blog': blog})


@login_required
def blog_add(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save()
            return blog.save_next(request)
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
    blog = Blog.get_detail(request, blog_id)
    confirm = False
    images = ContentImage.objects.filter(blog=blog)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)

        if 'delete_image' in request.POST:    # 紐づけ画像の削除
            ContentImage.delete_image(request)
        elif 'delete' in request.POST:        # 削除ボタンを押す
            if not images.exists():           # 紐づけ画像が存在しない
                confirm = True                # 確認画面へ
            else:                             # 紐づけ画像が存在する
                confirm = 'error'
        elif 'confirmed' in request.POST:     # 確認画面での選択
            if request.POST['confirmed'] == "はい":
                if not images.exists():        # 紐づけ画像が存在しない
                    blog.delete()             # 削除実行
                    return redirect('text_list')
                else:                         # 紐づけ画像が存在する
                    confirm = 'error'
        elif form.is_valid():                 # 内容変更の保存
            blog = form.save()
            return blog.save_next(request)

    else:
        form = BlogForm(instance=blog)

    context = {'form': form, 'blog_id': blog_id, 'confirm': confirm,
               'images': images}
    return TemplateResponse(request, 'blog/edit.html', context)


@login_required
def blog_text_list(request):
    blogs = Blog.get_list(request)
    blogs, page_info = get_pagination(request, blogs, per_page=30)
    page = page_info[0]
    page_max = page_info[1]
    page_range = page_info[2]
    context = {'blogs': blogs, 'page': page, 'page_max': page_max,
               'page_range': page_range}
    return TemplateResponse(request, 'blog/text_list.html', context)


@login_required
def image_upload(request):
    if request.method == 'POST':
        form = ContentImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            return redirect('edit', blog_id=image.blog.id)
    else:
        blog_id = request.GET.get('blog')
        if blog_id:
            form = ContentImageForm({'blog': blog_id})
        else:
            form = ContentImageForm()
    return TemplateResponse(request, 'blog/addImage.html', {'form': form})


@login_required
def image_list(request):
    blogs_inc_image = Blog.objects.filter(
        image__isnull=False
    ).exclude(image='').order_by('-published_at')
    content_images = ContentImage.objects.all().order_by('blog')
    blogs, c_imgs, page_info = page_for_two(
        request, blogs_inc_image, content_images, p_page_blogs=10,
        p_page_imgs=20
    )
    page = page_info[0]
    page_max = page_info[1]
    page_range = page_info[2]
    context = {'blogs': blogs, 'content_images': c_imgs,
               'page': page, 'page_max': page_max, 'page_range': page_range}
    return TemplateResponse(request, 'blog/image_list.html', context)
