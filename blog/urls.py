from django.urls import include, path
from blog import views

app_name = "blog"
urlpatterns = [
    path('blog/', views.blog_view, name="blog"),
    path('blog/category/', views.category_view, name="category"),
    path('blog/<slug:slug>', views.post_view, name="post"),
]
