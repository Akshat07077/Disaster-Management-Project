# Generated by Django 4.2.11 on 2024-06-21 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('disasters', '0003_disasterevent_latitude_disasterevent_longitude'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='available',
        ),
    ]