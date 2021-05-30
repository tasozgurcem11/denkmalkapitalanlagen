from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titel")
    header_image = models.ImageField(null=True, blank=True, upload_to="blog/headers/",
                                     verbose_name="Header-Bild")
    cover_image = models.ImageField(null=True, blank=True, upload_to="blog/covers/",
                                    verbose_name="Titelbild")
    description = models.CharField(max_length=200, blank=True, verbose_name="Beschreibung")
    content = models.TextField(null=True, blank=True, verbose_name="Inhalt")
    date = models.DateTimeField(default=timezone.now, verbose_name="Datum")
    slug = models.SlugField(default="", editable=False, max_length=255, null=False)

    # def clean(self):
    #     query = Post.objects.filter(slug=self.slug)
    #     if not query:
    #         err_msg = "Sie können keinen Beitrag mit einem vorhandenen Titel erstellen. Bitte ändern Sie den Titel."
    #         raise ValidationError({"title": err_msg})

    def __str__(self):
        stringify = "{}".format(self.title)
        return stringify

    def get_absolute_url(self):
        kwargs = {
            # "pk": self.id,
            "slug": self.slug
        }
        return reverse("blog:post", kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
