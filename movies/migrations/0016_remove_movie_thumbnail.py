# Generated by Django 4.0.4 on 2022-09-14 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0015_movie_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='thumbnail',
        ),
    ]