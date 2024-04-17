from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Comment

from  django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail #libreria para enviar correos

from .forms.blog.EmailPost import EmailPostFrom, CommentForm

from django.views.decorators.http import require_POST #implementacion del tipo de metodos de las vistas
# Create your views here.

#obtener todos los post
def list_post(req):
    
    post_all:object = Post.published.all() #busca totdos los post
    #TODO: creando el paginado
    paginator = Paginator(post_all,3)#se pagina de 3 en 3
    page_number = req.GET.get('page',1)#inicia en la pagina 1
    try:
        page_post = paginator.page(page_number)
    except EmptyPage:
        #si pasa un num no valido de paginacion pasa esto
        page_post = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        #si intentan pasar por url texto pasa esto
        page_post = paginator.page(1)
    template_path:str = 'Blog/post/list_post.html'#vistas html ruta
    context:dict = {    #data que mostrara  y  tranajara con los template
                'posts':page_post,
                }
    return render(req,template_path ,context) 

#detalle del post 
def detail_post(request, year, month, day, post):
    ''''
    1.- esta funcion get_object_or_404 nos evita usar un try exept.
    2-. esta condulta dice que: busca un post con el mismo id que te pasen,
        y cullo estatus este publicado
    '''
    post:object = get_object_or_404(Post,
                        status=Post.Status.PUBLISH,
                        slug=post,
                        publish__year=year,#extraccion del año, mes, dia
                        publish__month=month,
                        publish__day=day)
    comments = post.comments.filter(activate=True)
    form = CommentForm()
    template_path:str = 'Blog/post/detail.html'
    context:dict = {
                    'post_detail':post,
                    'form':form,
                    'comment':comments
                    }
    return render(request, template_path, context)

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status = Post.Status.PUBLISH)
    sent = False
    if request.method == 'POST':
        form = EmailPostFrom(request.POST)
        if form.is_valid():
            cd =form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())#espara tener una url como http:mysite.com/blog/2024/1/1 etc
            subject = f"{cd['name']} recpnmmends yuo read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n"\
                        f"{cd['name']}\'s comment {cd['comment']}"
            send_mail(subject, message, 'devengel1996@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostFrom()
    
    template_path = 'Blog/post/share.html'
    context = {
                'post':post,
                'form':form,
                'sent':sent
                }
    return render(request, template_path, context)

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISH)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)#con ese commit evitamos que se guarde por el momento ya que tenemos que agregar el post
        comment.post = post
        comment.save()
    
    template_url = 'Blog/post/comment.html'
    context = {
                'post':post,
                'form':form,
                'comment':comment
                }
    return render(request, template_url, context)