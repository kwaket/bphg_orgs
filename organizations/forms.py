from django import forms
from django.db import models
from django.db.models import Q

import django_filters

from .models import ApplicationScope, Employee, EmployeeRole, Organization, Project


class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ('name', 'country', 'address', 'site',
                  'activity_description')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(OrganizationForm, self).__init__(*args, **kwargs)


class ProjectForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['lead_scientist'].label = 'Ведущий научный сотрудник'
        self.fields['application_scope'].label = 'Область применения'

    lead_scientist = forms.CharField()
    application_scope = forms.CharField()

    class Meta:
        model = Project
        fields = ('name', 'organization', 'lead_scientist',
                  'application_scope', 'description', 'progress')


    def clean_lead_scientist(self):
        raw = self.cleaned_data.pop('lead_scientist')
        org = self.cleaned_data.get('organization')
        role = EmployeeRole.objects.filter(
            name='Ведущий научный сотрудник').first()
        scientists = Employee.objects.filter(role_id=role.id,
                                            organization_id=org.id).all()
        scientists = [s for s in scientists if s.name.lower() == raw.lower()]
        if scientists:
            scientist = scientists[0]
        else:
            scientist = Employee.objects.create(name=raw, role=role,
                organization=org, inserted_by=self.user)
        self.cleaned_data.update({'lead_scientist': scientist})
        return scientist

    def clean_application_scope(self):
        raw = self.cleaned_data.pop('application_scope')
        scopes = ApplicationScope.objects.all()
        scopes = [s for s in scopes if s.name.lower() == raw.lower()]
        if scopes:
            scope = scopes[0]
        else:
            scope = ApplicationScope.objects.create(name=raw,
                                                    inserted_by=self.user)
        return scope


class OrganizationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Organization
        fields = ['name', 'country']


class ProjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ['name', 'organization', 'lead_scientist', 'application_scope',
                  'progress']
