# Generated by Django 3.1.4 on 2020-12-20 09:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0005_auto_20201209_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='week',
            name='start_date',
            field=models.DateField(default=datetime.date(2020, 12, 21)),
        ),
    ]
