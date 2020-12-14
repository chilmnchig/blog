from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def make_range_ten(blogs, page, page_max):
    if page <= 5:
        blogs.pages = range(1, min(10, page_max) + 1)
    elif page >= page_max - 4:
        blogs.pages = range(max(1, page_max - 9),
                            page_max + 1
                            )
    else:
        blogs.pages = range(page - 5, page + 5)
    blogs.last = page_max
    return blogs


def get_pagination(request, blogs, per_page):
    page = request.GET.get('page', 1)
    paginator = Paginator(blogs, per_page)

    try:
        blogs = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        blogs = paginator.page(1)

    page = blogs.number
    page_max = paginator.num_pages
    blogs = make_range_ten(blogs, page, page_max)
    return blogs


def page_for_two(request, blogs, imgs, p_page_blogs, p_page_imgs):
    page = request.GET.get('page', 1)
    page = int(page)
    paginator_blogs = Paginator(blogs, p_page_blogs)
    paginator_imgs = Paginator(imgs, p_page_imgs)
    blogs_pages = paginator_blogs.num_pages
    imgs_pages = paginator_imgs.num_pages
    pages_list = [blogs_pages, imgs_pages]
    min_pages = min(pages_list)
    page_max = max(pages_list)

    if 1 <= page <= min_pages:
        blogs = paginator_blogs.page(page)
        imgs = paginator_imgs.page(page)
    elif blogs_pages < page <= imgs_pages:
        blogs = None
        imgs = paginator_imgs.page(page)
    elif imgs_pages < page <= blogs_pages:
        imgs = None
        blogs = paginator_blogs.page(page)
    else:
        page = 1
        blogs = paginator_blogs.page(1)
        imgs = paginator_imgs.page(1)

    blogs = make_range_ten(blogs, page, page_max)
    return blogs, imgs, page
