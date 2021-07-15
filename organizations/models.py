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
    name = models.CharField(max_length=500, verbose_name='Название')

    class Meta:
        verbose_name_plural='Страны'

    def __str__(self):
        return self.name


class Organization(UpdatingMixit):
    name = models.CharField(max_length=500, verbose_name='Название')
    country = models.ForeignKey(Country, verbose_name='Страна',
        on_delete=models.CASCADE)
    address = models.CharField(max_length=500, verbose_name='Адрес')
    site = models.CharField(max_length=500, verbose_name='Сайт')
    activity_description = models.CharField(max_length=500,
        verbose_name='Краткое описание вида деятельности', blank=True, null=True)

    class Meta:
        verbose_name_plural='Организации'
        unique_together = (('country', 'name'),)

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
