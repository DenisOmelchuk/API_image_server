# Generated by Django 4.2.6 on 2023-10-18 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_expiringlink_time_to_expired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expiringlink',
            name='time_to_expired',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
