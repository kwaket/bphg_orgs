from django.conf import settings
from django.db import models
from django.utils import timezone


class Country(models.Model):
    name = models.CharField(max_length=500, verbose_name='Название')

    inserted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='Добавил')
    inserted_at = models.DateTimeField(default=timezone.now,
        verbose_name='Добавлено')

    class Meta:
        verbose_name_plural='Страны'


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


class Organization(models.Model):
    name = models.CharField(max_length=500, verbose_name='Название')
    country = models.ForeignKey(Country, verbose_name='Страна',
        on_delete=models.CASCADE)
    city = models.ForeignKey(City, verbose_name='Город',
        on_delete=models.CASCADE)
    # projects
    site = models.CharField(max_length=500, verbose_name='Название')
    activity_description = models.CharField(max_length=500,
        verbose_name='Краткое описание вида деятельности')

    inserted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='Добавил')
    inserted_at = models.DateTimeField(default=timezone.now,
        verbose_name='Добавлено')

    class Meta:
        verbose_name_plural='Организации'


class EmployeeRole(models.Model):
    name = models.CharField(max_length=500, verbose_name='Название')

    inserted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='Добавил')
    inserted_at = models.DateTimeField(default=timezone.now,
        verbose_name='Добавлено')

    class Meta:
        verbose_name_plural='Должность'


class Employee(models.Model):
    name = models.CharField(max_length=500, verbose_name='Название')
    role = models.ForeignKey(EmployeeRole, verbose_name='Должность',
        on_delete=models.CASCADE)

    inserted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='Добавил')
    inserted_at = models.DateTimeField(default=timezone.now,
        verbose_name='Добавлено')

    class Meta:
        verbose_name_plural='Сотрудники'


class ApplicationScope(models.Model):
    name = models.CharField(max_length=500, verbose_name='Название')

    inserted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='Добавил')
    inserted_at = models.DateTimeField(default=timezone.now,
        verbose_name='Добавлено')

    class Meta:
        verbose_name_plural='Область применения'


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

    inserted_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name='Добавил')
    inserted_at = models.DateTimeField(default=timezone.now,
        verbose_name='Добавлено')

    class Meta:
        verbose_name_plural='Проекты'

