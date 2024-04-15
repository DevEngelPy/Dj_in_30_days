from django.contrib import admin
from .models import Post
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author', 'publish', 'status']#que mostrar en la tabla
    list_filter = ['status','created','publish', 'author']#espesifica5r el filtro
    search_fields = ['title','body']#campo de busqueda 
    prepopulated_fields = {'slug':('title',)}#el slug se llena automatica mente base al titulo (agilisar la creacion url)
    raw_id_fields = ['author']#
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']