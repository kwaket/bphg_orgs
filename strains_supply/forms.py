from django import forms
from django.db import models

from .models import Supply




class SupplyForm(forms.ModelForm):

    class Meta:
        model = Supply
        exclude = []
