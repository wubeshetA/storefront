# Generated by Django 4.2.1 on 2023-05-21 22:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
