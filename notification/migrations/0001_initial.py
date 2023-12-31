# Generated by Django 4.2.6 on 2024-01-06 05:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0014_shop_phone'),
        ('autofind', '0005_alter_slot_voice_call_number'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[(1, 'Bookings'), (2, 'Order')], max_length=1)),
                ('cart_item', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='shop.cartitem')),
                ('slot', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='autofind.slot')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
