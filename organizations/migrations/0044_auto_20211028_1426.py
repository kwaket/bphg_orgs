# Generated by Django 3.2.8 on 2021-10-28 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0043_auto_20211028_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='image',
            field=models.URLField(blank=True, max_length=2048, null=True, verbose_name='Ссылка на изображение'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='logo',
            field=models.URLField(blank=True, max_length=2048, null=True, verbose_name='Cсылка на логотип'),
        ),
    ]