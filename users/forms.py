from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django import forms

from .models import Profile

class UserForm(UserCreationForm):
    group = forms.ModelChoiceField(Group.objects.all())
    class Meta:
        model = User
        fields = ('username', 'first_name' , 'last_name', )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('company_branch',)
