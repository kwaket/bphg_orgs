from django import forms
from django.db import models

from .models import Organization


class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ('name', 'country', 'city', 'site',
                  'activity_description')
