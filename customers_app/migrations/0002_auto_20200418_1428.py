# Generated by Django 2.2.4 on 2020-04-18 14:28

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='orders',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.UUIDField(), blank=True, null=True, size=None),
        ),
    ]
