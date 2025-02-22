# Generated by Django 3.2.10 on 2021-12-20 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('strains_supply', '0003_alter_source_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='alias',
            field=models.CharField(default='kwa', max_length=500, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='city',
            name='inserted_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Добавлено'),
        ),
        migrations.AddField(
            model_name='city',
            name='inserted_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='Добавил'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='city',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Обновлено'),
        ),
        migrations.AddField(
            model_name='city',
            name='updated_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='strains_supply_city_related', to='auth.user', verbose_name='Обновил'),
            preserve_default=False,
        ),
    ]
