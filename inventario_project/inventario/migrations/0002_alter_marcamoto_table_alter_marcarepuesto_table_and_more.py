# Generated by Django 5.0.6 on 2024-07-11 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='marcamoto',
            table='marcamoto',
        ),
        migrations.AlterModelTable(
            name='marcarepuesto',
            table='marcarepuesto',
        ),
        migrations.AlterModelTable(
            name='modelo',
            table='modelo',
        ),
        migrations.AlterModelTable(
            name='pais',
            table='pais',
        ),
        migrations.AlterModelTable(
            name='proveedor',
            table='proveedor',
        ),
        migrations.AlterModelTable(
            name='repuesto',
            table='repuesto',
        ),
        migrations.AlterModelTable(
            name='repuestomodelo',
            table='repuestomodelo',
        ),
        migrations.AlterModelTable(
            name='unidadmedida',
            table='unidadmedida',
        ),
    ]
