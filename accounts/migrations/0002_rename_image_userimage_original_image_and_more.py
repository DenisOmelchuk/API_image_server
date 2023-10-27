# Generated by Django 4.2.6 on 2023-10-15 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userimage',
            old_name='image',
            new_name='original_image',
        ),
        migrations.AddField(
            model_name='userimage',
            name='thumbnail_image_200px',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
        migrations.AddField(
            model_name='userimage',
            name='thumbnail_image_400px',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
