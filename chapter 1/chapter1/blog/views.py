from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator,  EmptyPage, PageNotAnInteger

def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 3) #tres post por cada página
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # si no es un entero mandar la primera página
        posts = paginator.page(1)
    except EmptyPage:
        # si es la útlima, mandar el último resultado
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page':page, 'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
    publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post':post})


