# Generated by Django 4.2.6 on 2023-12-02 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autofind', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vc', models.IntegerField()),
                ('nc', models.IntegerField()),
            ],
        ),
    ]
