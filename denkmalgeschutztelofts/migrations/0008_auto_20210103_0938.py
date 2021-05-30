# Generated by Django 3.1.4 on 2021-01-03 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('denkmalgeschutztelofts', '0007_auto_20210102_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kontakt',
            name='quelle',
            field=models.CharField(choices=[('KT', 'Kontakt'), ('AK', 'Angebot Kaiser und Dicke'), ('AR', 'Angebot Rubenstrasse'), ('AT', 'Angebot Teschemacher Hof'), ('NS', 'Newsletter'), ('AN', 'Angebot'), ('RB', 'Rubenstrasse '), ('KD', 'Kaiser und Dicke'), ('TH', 'Teschemacher Hof'), ('IN', 'Home Page')], default='KT', max_length=2),
        ),
    ]
