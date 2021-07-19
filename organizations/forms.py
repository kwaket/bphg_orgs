from django import forms
from django.db import models
from django.db.models import Q

import django_filters

from .models import ApplicationScope, Employee, Organization, Project


class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ('name', 'countries', 'address', 'site', 'activity_description')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(OrganizationForm, self).__init__(*args, **kwargs)

    def clean_countries(self):
        countries= self.cleaned_data['countries']
        return countries

class ProjectForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['application_scope'].label = 'Область применения'

    application_scope = forms.CharField()

    class Meta:
        model = Project
        fields = ('name', 'organization', 'application_scope', 'description',
                  'progress')

    def clean_application_scope(self):
        raw = self.cleaned_data.pop('application_scope')
        scopes = ApplicationScope.objects.all()
        scopes = [s for s in scopes if s.name.lower() == raw.lower()]
        if scopes:
            scope = scopes[0]
        else:
            scope = ApplicationScope.objects.create(name=raw,
                inserted_by=self.user, updated_by=self.user)
        return scope


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'middle_name', 'degree', 'role',
                   'organization']


class LeadscientistForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'middle_name', 'degree']


class OrganizationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Organization
        fields = ['name', 'countries']


class ProjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ['name', 'organization', 'lead_scientist', 'application_scope',
                  'progress']
