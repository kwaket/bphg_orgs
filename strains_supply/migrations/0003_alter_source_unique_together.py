# Generated by Django 3.2.10 on 2021-12-17 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('strains_supply', '0002_auto_20211217_1234'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='source',
            unique_together={('name', 'city')},
        ),
    ]
