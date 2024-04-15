from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here

class Post(models.Model):#TODO modelo de un post
    #Todo este es un choice pero basado en clases
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISH = 'PB', 'Published'
    
    #atributos
    title = models.CharField(verbose_name="titulo", max_length=50)
    slug = models.SlugField(max_length=250)#url 
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
    class Meta:
        ordering = ["-publish"]#se ordenara del mas nuevo al mas viejo
        indexes = [
            models.Index(fields=["-publish"]),
        ]
        verbose_name = ("Post")
        verbose_name_plural = ("Posts")
    def __str__(self):
        return self.title
