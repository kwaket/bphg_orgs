# Generated by Django 3.2.5 on 2021-07-05 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0009_auto_20210705_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='organization',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='organizations.organization', verbose_name='Организация'),
            preserve_default=False,
        ),
    ]