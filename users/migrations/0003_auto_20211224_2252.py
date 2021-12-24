# Generated by Django 3.2.10 on 2021-12-24 19:52

from django.db import migrations


def add_persons(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('users', 'Profile')
    users = User.objects.filter(profile=None).all()
    for user in users:
        person = Profile.objects.create(user=user)
        person.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211223_1052'),
    ]

    operations = [
        migrations.RunPython(add_persons),
    ]
