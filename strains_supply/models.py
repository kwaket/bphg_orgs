from django.conf import settings
from django.utils import timezone
from django.db import models
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey

from strains_supply import utils


class InsertingMixin(models.Model):
    inserted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='Добавил')
    inserted_at = models.DateTimeField(default=timezone.now,
        verbose_name='Добавлено')

    class Meta:
        abstract = True


class UpdatingMixin(InsertingMixin):
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE, verbose_name='Обновил',
            related_name="%(app_label)s_%(class)s_related")

    updated_at = models.DateTimeField(default=timezone.now,
        verbose_name='Обновлено')

    class Meta:
        abstract = True

    name = models.CharField(max_length=500, verbose_name='Название')

    def __str__(self) -> str:
        return self.name


class Source(models.Model):
    name = models.CharField(max_length=1000, verbose_name='Название')
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.city.name}, {self.name}'

    class Meta:
        unique_together = ('name', 'city')

class CompanyBranch(models.Model):
    name = models.CharField(max_length=500, verbose_name='Название')

    def __str__(self) -> str:
        return self.name


class Supply(models.Model):
    source = models.ForeignKey(Source, verbose_name='Лечебное учреждение',
                               on_delete=models.PROTECT)
    dest = models.ForeignKey(CompanyBranch, verbose_name='Филиал',
                             on_delete=models.PROTECT)
    sent_at = models.DateTimeField(null=True, blank=True,
                                   verbose_name='Предполагаемая дата отправки')
    num = models.DateTimeField(null=True, blank=True,
                               verbose_name='Предполагаемое количество')
    recieved_at = models.DateTimeField(null=True, blank=True,
                                       verbose_name='Дата приема')
    recieved_remark = models.CharField(max_length=500, null=True, blank=True,
                                       verbose_name='Примичание при приеме')


class Strain(models.Model):
    name = CharField(max_length=500)


class SupplyContent(models.Model):
    supply_id = ForeignKey(Supply, on_delete=models.PROTECT)
    strain_id = ForeignKey(Strain, on_delete=models.PROTECT)
    num = models.IntegerField(default=0)

