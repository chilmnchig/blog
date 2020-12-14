from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_pagination(request, blogs, per_page):
    page = request.GET.get('page')
    paginator = Paginator(blogs, per_page)

    try:
        blogs = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        blogs = paginator.page(1)
    for blog in blogs:
        blog.info_content()
    if blogs.number <= 5:
        blogs.pages = range(1, min(10, paginator.num_pages) + 1)
    elif blogs.number >= paginator.num_pages - 4:
        blogs.pages = range(max(1, paginator.num_pages - 9),
                            paginator.num_pages + 1
                            )
    else:
        blogs.pages = range(blogs.number - 5, blogs.number + 5)
    blogs.last = paginator.num_pages
    return blogs
