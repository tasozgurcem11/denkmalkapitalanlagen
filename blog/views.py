from django.shortcuts import render

from blog.models import Post


# Create your views here.
def blog_view(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "blog/blog.html", context)


def category_view(request):
    context = {}
    return render(request, "blog/category.html", context)


def post_view(request, slug):
    try:
        post = Post.objects.filter(slug=slug)[0]
    except IndexError:
        post = None
    context = {"post": post}
    return render(request, "blog/post.html", context)
