# Generated by Django 3.1.2 on 2023-05-15 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_carrito_cantidad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrito',
            name='cantidad',
        ),
    ]
