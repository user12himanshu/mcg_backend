# Generated by Django 4.2.6 on 2023-12-24 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='quanitity_in_stock',
            field=models.IntegerField(default=0),
        ),
    ]
