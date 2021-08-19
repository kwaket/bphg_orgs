from django.conf import settings
from django.db import models
from django.db.models import fields, indexes
from django.utils import timezone

from computed_property import ComputedTextField


class InsertingMixin(models.Model):
    inserted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='Добавил')
    inserted_at = models.DateTimeField(default=timezone.now,
        verbose_name='Добавлено')

    class Meta:
        abstract = True

class UpdatingMixit(InsertingMixin):
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE, verbose_name='Обновил',
            related_name="%(app_label)s_%(class)s_related")

    updated_at = models.DateTimeField(default=timezone.now,
        verbose_name='Обновлено')

    class Meta:
        abstract = True

class Country(InsertingMixin):
    name = models.CharField(max_length=500, verbose_name='Название',
        unique=True)
    fullname = models.CharField(max_length=500,
        verbose_name='Полное наименование', null=True, blank=True)
    english	 = models.CharField(max_length=500, verbose_name='На английском',
        unique=True)
    alpha2 = models.CharField(max_length=2, verbose_name='Alpha2',
        null=True, blank=True, unique=True)
    alpha3 = models.CharField(max_length=3, verbose_name='Alpha3',
        unique=True)
    iso	 = models.IntegerField(verbose_name='ISO', unique=True)
    location = models.CharField(max_length=500, verbose_name='Часть света',
        null=True, blank=True)
    location_precise = models.CharField(max_length=500,
        verbose_name='Расположение')

    class Meta:
        verbose_name_plural='Страны'

    def __str__(self):
        return self.name

class Organization(UpdatingMixit):

    class FieldOfActivity(models.TextChoices):
        VETERINARY_MEDICINE = 'VM', 'Ветеринария'
        RESEARCH = 'RS', 'Исследования'
        PRODUCTION_OF_DRUGS = 'PD', 'Производство препаратов'
        INNOVATIVE_PRODUCTS = 'IP', 'Инновационные продукты на основе бактериофагов'

    name = models.CharField(max_length=500, verbose_name='Название')
    countries = models.ManyToManyField(Country, verbose_name='Страна')
    address = models.CharField(max_length=500, verbose_name='Адрес')
    site = models.CharField(max_length=500, verbose_name='Сайт')
    activity_description = models.TextField(max_length=2048,
        verbose_name='Краткое описание вида деятельности', blank=True,
        null=True)
    field_of_activity = models.CharField(max_length=2,
        choices=FieldOfActivity.choices, blank=True, null=True,
        verbose_name='Сфера деятельности')
    products = models.TextField(max_length=2048, verbose_name='Продукция',
        null=True, blank=True)

    class Meta:
        verbose_name_plural='Организации'
        unique_together = (('name', 'address'),)

    def __str__(self):
        return self.name


class EmployeeRole(UpdatingMixit):
    name = models.CharField(max_length=500, verbose_name='Название')

    class Meta:
        verbose_name_plural='Должность'

    def __str__(self):
        return self.name


class Employee(UpdatingMixit):
    first_name = models.CharField(max_length=200, verbose_name='Имя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=200, verbose_name='Отчество',
        null=True, blank=True)
    degree = models.CharField(max_length=500, verbose_name='Ученная степень')
    role = models.ForeignKey(EmployeeRole, verbose_name='Должность',
        on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, verbose_name='Организация',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        unique_together = (('first_name', 'last_name', 'degree'),)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        middle_name = self.middle_name or ''
        return '{} {} {}'.format(self.last_name, self.first_name,
                                 middle_name).strip()


class ApplicationScope(UpdatingMixit):
    name = models.CharField(max_length=500, verbose_name='Название')

    class Meta:
        verbose_name_plural='Область применения'

    def __str__(self):
        return self.name


class Progress(UpdatingMixit):
    name = models.CharField(max_length=200, verbose_name='Название')

    class Meta:
        verbose_name_plural='Уровень прогресса'

    def __str__(self):
        return self.name


class Project(UpdatingMixit):
    name = models.CharField(max_length=500, verbose_name='Название')
    lead_scientist = models.ForeignKey(Employee,
        verbose_name='Ведущий научный сотрудник',
        on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization,
        verbose_name='Огранизация',
        on_delete=models.CASCADE)
    application_scope = models.ForeignKey(ApplicationScope,
        verbose_name='Область применения', on_delete=models.CASCADE)
    description = models.CharField(max_length=1000,
        verbose_name='Описание')
    progress = models.ForeignKey(Progress, verbose_name='Уровень прогресса',
        on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural='проекты'

    def __str__(self):
        return self.name
