# Generated by Django 4.2.6 on 2023-12-28 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostic', '0006_diagnosticvideos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diagnosticvideos',
            name='file',
        ),
        migrations.AddField(
            model_name='diagnosticvideos',
            name='url',
            field=models.URLField(default='', max_length=500),
        ),
    ]