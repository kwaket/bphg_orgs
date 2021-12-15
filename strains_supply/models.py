from django.db import models
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey


class City(models.Model):
    name = models.CharField(max_length=500, verbose_name='Название')


class Source(models.Model):
    name = models.CharField(max_length=1000, verbose_name='Название')


class CompanyBranch(models.Model):
    name = models.CharField(max_length=500, verbose_name='Название')


class Supply(models.Model):
    source = models.ForeignKey(Source, verbose_name='Лечебное учреждение',
                               on_delete=models.PROTECT)
    source_city = models.ForeignKey(City, verbose_name='Город', on_delete=models.PROTECT)
    dest = models.ForeignKey(CompanyBranch, verbose_name='Филиал', on_delete=models.PROTECT)
    sent_at = models.DateTimeField(null=True, blank=True,
                                   verbose_name='Предполагаемая дата отправки')
    recieved_at = models.DateTimeField(null=True, blank=True,
                                       verbose_name='Дата приема')
    recieved_remark = models.CharField(max_length=500, null=True, blank=True,
                                       verbose_name='Примичание при приеме')
    num = models.DateTimeField(null=True, blank=True,
                               verbose_name='Предполагаемое количество')


class Strain(models.Model):
    name = CharField(max_length=500)


class SupplyContent(models.Model):
    supply_id = ForeignKey(Supply, on_delete=models.PROTECT)
    strain_id = ForeignKey(Strain, on_delete=models.PROTECT)
    num = models.IntegerField(default=0)

