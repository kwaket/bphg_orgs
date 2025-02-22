# Generated by Django 3.2.10 on 2021-12-23 11:00

from django.db import migrations


def get_permissions(apps):
    Permission = apps.get_model('auth', 'Permission')
    model_names = ['companybranch', 'city', 'strain', 'source']
    perms = []
    for model_name in model_names:
        for mod in ['add_', 'view_', 'change_']:
            perms.append(mod + model_name)
    perms = Permission.objects.filter(codename__in=perms)
    return perms


def add_strains_group(apps, schema_editor):
    permissions = get_permissions(apps)
    Group = apps.get_model('auth', 'Group')
    groups = [
        {'name': 'Поставки (Администратор)'},
        {'name': 'Поставки (Прием)'}
    ]
    for group in groups:
        g = Group.objects.create(name = group['name'])
        g.permissions.set(permissions)
        g.save()


class Migration(migrations.Migration):

    dependencies = [
        ('strains_supply', '0013_auto_20211222_2231'),
    ]

    operations = [
        migrations.RunPython(add_strains_group),
    ]
