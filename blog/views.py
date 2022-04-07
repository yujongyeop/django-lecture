from django.shortcuts import render

# Create your views here.
from blog.models import Post


def index(request):
    posts = Post.objects.all().order_by('-pk')
    return render(request, 'blog/index.html', {'posts': posts})


def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)
    context ={'post': post,}
    return render(request, 'blog/single_post_page.html', context=context)