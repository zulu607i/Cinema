# Generated by Django 4.0.4 on 2022-08-03 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0012_alter_movie_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.URLField(verbose_name='Poster'),
        ),
    ]
