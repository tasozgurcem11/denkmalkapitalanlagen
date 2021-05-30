# Generated by Django 3.1.1 on 2020-11-23 20:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Titel')),
                ('header_image', models.ImageField(blank=True, null=True, upload_to='blog/headers/', verbose_name='Header-Bild')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='blog/covers/', verbose_name='Titelbild')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='Beschreibung')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Inhalt')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Datum')),
                ('slug', models.SlugField(default='', editable=False, max_length=255)),
            ],
        ),
    ]
