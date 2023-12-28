# Generated by Django 4.2.6 on 2023-12-28 00:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_rename_half_yaer_shopsubscriptioncharges_half_yearly'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiagnosticSubscriptionCharges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthly', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quarterly', models.DecimalField(decimal_places=2, max_digits=10)),
                ('half_yearly', models.DecimalField(decimal_places=2, max_digits=10)),
                ('yearly', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='DiagnosticSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_till', models.DateField(blank=True, null=True)),
                ('date_added', models.DateTimeField(blank=True, null=True)),
                ('type', models.CharField(blank=True, max_length=300, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
