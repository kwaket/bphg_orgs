# Generated by Django 3.2.5 on 2021-08-09 10:26

from django.db import migrations
from django.contrib.auth.models import Group


def populate_progress(apps, schema_editor):
    Data = apps.get_model('auth', 'Group')
    data = [
        {'name': 'Пользователи'},
        {'name': 'Модераторы'},
        ]
    for group in data:
        Data.objects.create(name=group['name'])


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0033_auto_20210809_1239'),
    ]

    operations = [
        migrations.RunPython(populate_progress)
    ]
