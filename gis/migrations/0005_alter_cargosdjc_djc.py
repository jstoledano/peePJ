# Generated by Django 5.1.5 on 2025-01-31 16:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gis', '0004_cargosdjc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargosdjc',
            name='djc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis.djc'),
        ),
    ]
