# Generated by Django 4.2.6 on 2023-10-18 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_expiringlink_time_to_expired'),
    ]

    operations = [
        migrations.AddField(
            model_name='expiringlink',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
