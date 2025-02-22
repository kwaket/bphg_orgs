# Generated by Django 3.2.8 on 2021-10-28 06:21

from django.db import migrations


def fill_logo_field(apps, schema_editor):
    Organization = apps.get_model('organizations', 'Organization')
    for org in Organization.objects.all():
        if not org.logo and org.image:
            org.logo = org.image
            org.save() 


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0040_organization_logo'),
    ]

    operations = [
        migrations.RunPython(fill_logo_field)
    ]
