# Generated by Django 5.1.5 on 2025-01-23 17:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entidad', models.PositiveSmallIntegerField()),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DJP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('djp', models.PositiveSmallIntegerField()),
                ('nombre', models.CharField(max_length=100)),
                ('entidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis.entidad')),
            ],
        ),
        migrations.CreateModel(
            name='DJC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('djc', models.PositiveSmallIntegerField()),
                ('nombre', models.CharField(max_length=100)),
                ('entidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis.entidad')),
            ],
        ),
        migrations.CreateModel(
            name='Distrito_Local',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distrito_local', models.PositiveSmallIntegerField()),
                ('entidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis.entidad')),
            ],
        ),
        migrations.CreateModel(
            name='Distrito_Federal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distrito_federal', models.PositiveSmallIntegerField()),
                ('entidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis.entidad')),
            ],
        ),
        migrations.CreateModel(
            name='ARE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('are', models.PositiveSmallIntegerField()),
                ('activa', models.BooleanField(default=True)),
                ('entidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis.entidad')),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('municipio', models.PositiveSmallIntegerField()),
                ('nombre', models.CharField(max_length=100)),
                ('djc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis.djc')),
                ('djp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis.djp')),
                ('entidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis.entidad')),
            ],
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seccion', models.PositiveSmallIntegerField()),
                ('tipo', models.PositiveSmallIntegerField(choices=[(2, 'URBANA'), (3, 'MIXTA'), (4, 'RURAL')])),
                ('activa', models.BooleanField(default=True)),
                ('are', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis.are')),
                ('distrito_federal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis.distrito_federal')),
                ('distrito_local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis.distrito_local')),
                ('entidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis.entidad')),
                ('municipio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis.municipio')),
            ],
        ),
        migrations.CreateModel(
            name='ZORE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zore', models.PositiveSmallIntegerField()),
                ('activa', models.BooleanField(default=True)),
                ('entidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis.entidad')),
            ],
        ),
        migrations.AddField(
            model_name='are',
            name='zore',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis.zore'),
        ),
    ]
