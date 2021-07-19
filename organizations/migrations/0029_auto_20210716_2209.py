# Generated by Django 3.2.5 on 2021-07-16 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0028_alter_employee_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'verbose_name': 'Сотрудник', 'verbose_name_plural': 'Сотрудники'},
        ),
        migrations.AddField(
            model_name='organization',
            name='countries',
            field=models.ManyToManyField(to='organizations.Country', verbose_name='Страна'),
        ),
        migrations.AlterUniqueTogether(
            name='organization',
            unique_together={('name', 'address')},
        ),
        migrations.RemoveField(
            model_name='organization',
            name='country',
        ),
    ]
