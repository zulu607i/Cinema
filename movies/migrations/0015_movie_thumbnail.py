# Generated by Django 4.0.4 on 2022-09-08 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0014_alter_movie_poster'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='thumbnail',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to='thumbnails'),
        ),
    ]
