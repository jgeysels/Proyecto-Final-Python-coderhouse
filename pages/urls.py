from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('pages/', views.pages, name='pages'),
    path('pages/<int:page_id>/', views.page_detail, name='page_detail'),
    path('create_blog/', views.create_blog, name='create_blog'),
    path('update_blog/<int:blog_id>/', views.update_blog, name='update_blog'),
    path('delete_blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
]