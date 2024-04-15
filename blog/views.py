from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.

#obtener todos los post
def list_post(req):
    
    post_all:object = Post.objects.all() #busca totdos los post
    
    template_path:str = 'Blog/post/list_post.html'#vistas html ruta
    context:dict = {    #data que mostrara  y  tranajara con los template
                'posts':post_all,
                }
    return render(req,template_path ,context) 

#detalle del post 
def detail_post(req, pk:int):
    ''''
    1.- esta funcion get_object_or_404 nos evita usar un try exept.
    2-. esta condulta dice que: busca un post con el mismo id que te pasen,
        y cullo estatus este publicado
    '''
    post:object = get_object_or_404(Post,
                        id=id,
                        status=Post.Status.PUBLISH)
    template_path:str = 'Blog/post/datail.html'
    context:dict = {
                    'post_detail':post,
                    }
    return render(req, template_path, context)