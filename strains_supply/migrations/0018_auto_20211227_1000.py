# Generated by Django 3.2.10 on 2021-12-27 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('strains_supply', '0017_auto_20211227_0945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplycontent',
            name='num',
        ),
        migrations.AddField(
            model_name='supplycontent',
            name='bacteria_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='strains_supply.bacteriatype'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='supplycontent',
            name='strain',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Штамм'),
        ),
    ]
