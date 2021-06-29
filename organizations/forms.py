from django import forms
from django.db import models

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
