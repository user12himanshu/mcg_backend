# Generated by Django 4.2.6 on 2023-12-28 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostic', '0007_remove_diagnosticvideos_file_diagnosticvideos_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnostic',
            name='type',
            field=models.CharField(choices=[('wiring', 'Wiring'), ('diagnostic', 'Diagnostic'), ('maintenance', 'Maintenance')], default=('diagnostic', 'Diagnostic'), max_length=100),
        ),
    ]