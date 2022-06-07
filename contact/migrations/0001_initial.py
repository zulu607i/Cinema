# Generated by Django 4.0.4 on 2022-06-07 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cinemas', '0008_remove_hall_seats_remove_movietheater_halls_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Full name')),
                ('email', models.EmailField(max_length=100, verbose_name='Email')),
                ('phone_number', models.CharField(max_length=100, verbose_name='Phone number')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('subject', models.CharField(max_length=100, verbose_name='Subject')),
                ('message', models.TextField(max_length=300, verbose_name='Message')),
                ('cinema', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cinemas.movietheater', verbose_name='Cinema')),
            ],
        ),
    ]
