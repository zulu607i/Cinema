# Generated by Django 4.0.4 on 2022-06-14 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinemas', '0009_alter_seat_seat_nr_alter_seat_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='seat',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='hall',
            name='rows',
            field=models.IntegerField(default=15),
        ),
        migrations.AddField(
            model_name='hall',
            name='seats_per_row',
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name='seat',
            name='seat_name',
            field=models.CharField(default='A1', max_length=4),
        ),
        migrations.RemoveField(
            model_name='seat',
            name='is_reserved',
        ),
        migrations.RemoveField(
            model_name='seat',
            name='seat_nr',
        ),
        migrations.RemoveField(
            model_name='seat',
            name='seat_row',
        ),
    ]