# Generated by Django 4.0.4 on 2022-06-08 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinemas', '0009_alter_seat_seat_nr_alter_seat_unique_together'),
        ('reservation', '0005_alter_playingtime_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='playing_time',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reservation.playingtime', verbose_name='Cinema/Hall/Date'),
        ),
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('seat', 'playing_time')},
        ),
    ]
