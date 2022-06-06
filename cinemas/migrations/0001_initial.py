# Generated by Django 4.0.4 on 2022-06-02 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_nr', models.PositiveIntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MovieTheater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('Street', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.street')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.city')),
                ('county', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.county')),
                ('halls', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cinemas.hall')),
            ],
        ),
        migrations.AddField(
            model_name='hall',
            name='seats',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cinemas.seat'),
        ),
    ]