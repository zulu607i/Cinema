# Generated by Django 4.0.4 on 2022-06-06 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_alter_movie_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='movie',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='movie',
            name='date_scheduled_at',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='hall_is_playing',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='time_scheduled_at',
        ),
    ]