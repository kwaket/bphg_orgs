# Generated by Django 3.2.5 on 2021-07-14 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0022_alter_organization_updated_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='inserted_at',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='inserted_by',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='updated_by',
        ),
    ]
