# Generated by Django 4.0.4 on 2022-10-06 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0013_reservation_expired'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='price',
            field=models.FloatField(default=20.0),
        ),
        migrations.AddField(
            model_name='reservation',
            name='stripe_price_id',
            field=models.CharField(default='price_1LptmkGMvPFpBlyfXSbzeFXF', max_length=500),
        ),
    ]