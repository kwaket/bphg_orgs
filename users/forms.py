from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.db import models
from django import forms


class UserCreateForm(UserCreationForm):
    group = forms.ModelChoiceField(Group.objects.all())
    class Meta:
        model = User
        fields = ('username', 'first_name' , 'last_name', )
