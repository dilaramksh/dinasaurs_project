# Generated by Django 4.2.18 on 2025-03-18 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='society',
            name='logo',
            field=models.ImageField(blank=True, default='society_logos/default.jpg', null=True, upload_to='society_logos/'),
        ),
    ]
