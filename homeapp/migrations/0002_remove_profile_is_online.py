# Generated by Django 5.0.2 on 2024-04-07 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_online',
        ),
    ]
