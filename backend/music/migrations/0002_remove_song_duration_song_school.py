# Generated by Django 5.0.2 on 2025-03-16 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='duration',
        ),
        migrations.AddField(
            model_name='song',
            name='school',
            field=models.CharField(default='未知流派', max_length=255),
        ),
    ]
