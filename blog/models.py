from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User #modelo por defecto de user 
from django.urls import reverse #coneste se puede asignar una url acada uno delos atributos
# Create your models here

'''
    este modelo es una query o una peticion la cual
    pide todos los post pulicados
    ! se usara en el modelo post y asi usarala en la views
    
    NOTA: se podria reducir vastante codigo en las views, en el caso de
    las peticiones db
'''
class PublisheManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset()\
                        .filter(status=Post.Status.PUBLISH)

class Post(models.Model):#TODO modelo de un post
    #Todo este es un choice pero basado en clases
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISH = 'PB', 'Published'
    
    #atributos
    title = models.CharField(verbose_name="titulo", max_length=50)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')#url 
    author = models.ForeignKey(User, verbose_name="usuario",
                                on_delete=models.CASCADE,
                                related_name='blog_posts')
    body = models.TextField(verbose_name="body...")
    publish = models.DateTimeField(default=timezone.now)#publicacion de la sona en que esta
    created = models.DateTimeField(auto_now_add=True)#fecha de creacion automatica
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                                choices=Status.choices,
                                default=Status.DRAFT)
    objects = models.Manager()
    published = PublisheManager() #modelo creado arriba
    class Meta:
        ordering = ["-publish"]#se ordenara del mas nuevo al mas viejo
        indexes = [
            models.Index(fields=["-publish"]),
        ]
        verbose_name = ("Post")
        verbose_name_plural = ("Posts")
    def __str__(self):
        return self.title
    
    '''
    este es pra url canonicas las cuales remplasa alas url de html list_post por este metodo
    '''
    def get_absolute_url(self):
        return reverse('blog:detail_post',args=[self.publish.year,
                                                self.publish.month,
                                                self.publish.day,
                                                self.slug
                                                ])
class Comment(models.Model):

    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(("nombre"), max_length=50)
    email = models.EmailField(("email"), max_length=254)
    body = models.TextField(("body"))
    created = models.DateTimeField((""), auto_now=False, auto_now_add=True)
    update = models.DateTimeField((""), auto_now=True, auto_now_add=False)
    activate = models.BooleanField(("activo?"), default=True)
    class Meta:
        verbose_name = ("Comment")
        verbose_name_plural = ("Comments")

    def __str__(self):
        return f" coment by {self.name} on {self.post}"

    def get_absolute_url(self):
        return reverse("Comment_detail", kwargs={"pk": self.pk})
