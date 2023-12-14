# Generated by Django 4.2.6 on 2023-11-22 23:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_customuser_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='media/profile_photo/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])]),
        ),
    ]
