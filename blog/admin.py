from django.contrib import admin
from blog.models import Post
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.
# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    fields = (
        "title",
        ("header_image", "cover_image"),
        "description",
        "content",
        "date",
    )
    summernote_fields = ("content",)
