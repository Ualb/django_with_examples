from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator,  EmptyPage, PageNotAnInteger
from django.core.mail import send_mail


from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

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
    post = get_object_or_404(Post, 
                            slug=post, 
                            status='published', 
                            publish__year=year,
                            publish__month=month, 
                            publish__day=day)

    # lista de los comentarios activos para este post
    comments = post.comments.filter(active=True)
    new_comment = None
    
    if request.method == 'POST':
        # un comentario fue posteado
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # crear un objeto de comentario pero no guardarlo en la bd
            new_comment = comment_form.save(commit=False)
            # asignar el actual comentario al post
            new_comment.post = post
            # guardar el comentario
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 
                'blog/post/detail.html', 
                {'post': post,
                'comments': comments,
                'new_comment': new_comment,
                'comment_form': comment_form})

def post_share(request, post_id):
    # obtener post por id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # el formulario fue suministrado
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # el formulario pasa la validación de sus campos
            cd = form.cleaned_data
            # enviar el correo
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'ulises050794@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})

