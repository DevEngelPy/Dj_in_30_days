from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.list_post, name='lista_post'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.detail_post, name='detail_post'),
]
