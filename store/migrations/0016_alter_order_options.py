# Generated by Django 4.2.1 on 2023-05-23 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_remove_customer_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can cancel order')]},
        ),
    ]