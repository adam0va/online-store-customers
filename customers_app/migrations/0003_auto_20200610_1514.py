# Generated by Django 2.2.4 on 2020-06-10 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers_app', '0002_auto_20200418_1428'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='surname',
        ),
        migrations.AddField(
            model_name='customer',
            name='login',
            field=models.CharField(default='0', max_length=50),
        ),
    ]