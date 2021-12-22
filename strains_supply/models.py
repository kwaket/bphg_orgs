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


class AliasMixin(models.Model):
    def save(self, **kwargs):
        self.alias = utils.get_alias(self.name)
        super().save(**kwargs)

    class Meta:
        abstract = True


class City(UpdatingMixin, AliasMixin):
    alias = models.CharField(max_length=500, unique=True)
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


class CompanyBranch(UpdatingMixin, AliasMixin):
    alias = models.CharField(max_length=500, unique=True)
    name = models.CharField(max_length=500, verbose_name='Название')

    def __str__(self) -> str:
        return self.name


class Supply(UpdatingMixin):
    source = models.ForeignKey(Source, verbose_name='Лечебное учреждение',
                               on_delete=models.PROTECT)
    dest = models.ForeignKey(CompanyBranch, verbose_name='Филиал',
                             on_delete=models.PROTECT)
    suggested_sent_date = models.DateField(null=True, blank=True,
                                   verbose_name='Предполагаемая дата отправки')
    suggested_num = models.IntegerField(null=True, blank=True,
                               verbose_name='Предполагаемое количество')
    sent_at = models.DateField(null=True, blank=True,
                               verbose_name='Фактическа дата отправки')
    num = models.IntegerField(null=True, blank=True, verbose_name='Количество')
    received_at = models.DateTimeField(null=True, blank=True,
                                       verbose_name='Дата приема')
    received_remark = models.CharField(max_length=500, null=True, blank=True,
                                       verbose_name='Примичание при приеме')


class Strain(models.Model):
    name = CharField(max_length=500)

    def __str__(self):
        return self.name


class SupplyContent(models.Model):
    supply_id = ForeignKey(Supply, on_delete=models.PROTECT)
    strain_id = ForeignKey(Strain, on_delete=models.PROTECT)
    num = models.IntegerField(default=0)

