# Generated by Django 4.2.6 on 2023-12-25 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostic', '0002_rename_carbrands_carbrand_rename_carmodels_carmodel_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EngineType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='diagnostic.caryear')),
            ],
        ),
        migrations.AddField(
            model_name='diagnostic',
            name='engine_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='diagnostic.enginetype'),
        ),
    ]
