# Generated by Django 4.2.18 on 2025-03-09 14:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocietyColorHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_colour1', models.CharField(max_length=7)),
                ('previous_colour2', models.CharField(max_length=7)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('society', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color_history', to='social_media.society')),
            ],
        ),
    ]
