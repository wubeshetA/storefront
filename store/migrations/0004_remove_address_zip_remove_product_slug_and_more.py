# Generated by Django 4.2.1 on 2023-05-10 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_address_zip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='zip',
        ),
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
        migrations.AddField(
            model_name='product',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
    ]
