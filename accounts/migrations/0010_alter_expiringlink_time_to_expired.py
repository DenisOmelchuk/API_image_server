# Generated by Django 4.2.6 on 2023-10-18 22:27

import accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_expiringlink_time_to_expired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expiringlink',
            name='time_to_expired',
            field=models.IntegerField(blank=True, null=True, validators=[accounts.validators.validate_time_to_expired]),
        ),
    ]
