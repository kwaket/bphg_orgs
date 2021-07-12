from django.conf import settings
from django.db import models
from django.db.models import indexes
from django.utils import timezone


class Country(models.Model):
    name = models.CharField(max_length=500, verbose_name='Название')

    inserted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='Добавил')
    inserted_at = models.DateTimeField(default=timezone.now,
        verbose_name='Добавлено')

    class Meta:
        verbose_name_plural='Страны'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=500, verbose_name='Название')
    country = models.ForeignKey(Country, verbose_name='Страна',
        on_delete=models.CASCADE)

    inserted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='Добавил')
    inserted_at = models.DateTimeField(default=timezone.now,
        verbose_name='Добавлено')

    class Meta:
        verbose_name_plural='Города'

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=500, verbose_name='Название')
    country = models.ForeignKey(Country, verbose_name='Страна',
        on_delete=models.CASCADE)
    city = models.ForeignKey(City, verbose_name='Город',
        on_delete=models.CASCADE)
    # projects
    site = models.CharField(max_length=500, verbose_name='Сайт')
    activity_description = models.CharField(max_length=500,
        verbose_name='Краткое описание вида деятельности', blank=True, null=True)

    inserted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='Добавил')
    inserted_at = models.DateTimeField(default=timezone.now,
        verbose_name='Добавлено')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='обновил',
        related_name='updated_organization')
    updated_at = models.DateTimeField(default=timezone.now,
        verbose_name='Обновлено')


    class Meta:
        verbose_name_plural='Организации'
        unique_together = (('country', 'name'),)

    def __str__(self):
        return self.name


class EmployeeRole(models.Model):
    name = models.CharField(max_length=500, verbose_name='Название')

    inserted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='Добавил')
    inserted_at = models.DateTimeField(default=timezone.now,
        verbose_name='Добавлено')

    class Meta:
        verbose_name_plural='Должность'

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=500, verbose_name='Название')
    role = models.ForeignKey(EmployeeRole, verbose_name='Должность',
        on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, verbose_name='Организация',
        on_delete=models.CASCADE)

    inserted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='Добавил')
    inserted_at = models.DateTimeField(default=timezone.now,
        verbose_name='Добавлено')

    class Meta:
        verbose_name_plural='Сотрудники'

    def __str__(self):
        return self.name


class ApplicationScope(models.Model):
    name = models.CharField(max_length=500, verbose_name='Название')

    inserted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='Добавил')
    inserted_at = models.DateTimeField(default=timezone.now,
        verbose_name='Добавлено')

    class Meta:
        verbose_name_plural='Область применения'

    def __str__(self):
        return self.name


class Progress(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')

    inserted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='Добавил')
    inserted_at = models.DateTimeField(default=timezone.now,
        verbose_name='Добавлено')

    def __str__(self):
        return self.name


class Project(models.Model):
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

    inserted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='Добавил')
    inserted_at = models.DateTimeField(default=timezone.now,
        verbose_name='Добавлено')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='обновил',
        related_name='updated_project')
    updated_at = models.DateTimeField(default=timezone.now,
        verbose_name='Обновлено')


    class meta:
        verbose_name_plural='проекты'

    def __str__(self):
        return self.name
