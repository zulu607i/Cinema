# Generated by Django 4.0.4 on 2022-07-19 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0011_alter_movie_imdb_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='Description'),
        ),
    ]
