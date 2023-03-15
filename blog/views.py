from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm,NewUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



def post_list(request):
    posts=Post.objects.order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts':posts}) #El nombre de posts luego se usa en el HTML, justamente hace referencia a esta vista.

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user=request.user
    return render(request, 'blog/post_detail.html', {'post': post,'user':user})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user!=post.author:
        return redirect('post_list')
    else:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('my_post')
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_delete(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user!=post.author:
        return redirect('post_list')
    else:
        post.delete_post()
        return redirect('my_post')

def sign_up(request):
    form = NewUserForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Tu cuenta ha sido creada exitosamente.')
        return redirect('login')
    context = {
        'form': form
            }
    return render(request, 'blog/new_user.html', context)

@login_required
def my_post(request):
    posts=Post.objects.filter(author=request.user).order_by('-published_date')
    return render(request, 'blog/my_post.html', {'posts':posts})
