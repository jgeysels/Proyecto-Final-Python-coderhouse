from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Blog
from .forms import BlogForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def index(request):
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')

def pages(request):
    blogs = Blog.objects.all()
    return render(request, 'pages/pages.html', {'blogs': blogs})

def page_detail(request, page_id):
    blog = get_object_or_404(Blog, pk=page_id)
    return render(request, 'pages/page_detail.html', {'blog': blog})

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)  
            blog.author = request.user  
            blog.save()  
            return redirect('pages')
    else:
        form = BlogForm()
    return render(request, 'pages/create_blog.html', {'form': form})

@login_required
def update_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    
    if request.user != blog.author and not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('page_detail', blog_id)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'pages/update_blog.html', {'form': form, 'blog': blog})


@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    
    if request.user != blog.author and not request.user.is_superuser:
        raise PermissionDenied

    blog.delete()
    return redirect('pages')