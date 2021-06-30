from django import forms
from django.db import models

import django_filters

from .models import Organization, Project


class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ('name', 'country', 'city', 'site',
                  'activity_description')


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'lead_scientist', 'organization',
                  'application_scope', 'description', 'progress')


class OrganizationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Organization
        fields = ['name', 'country', 'city']
