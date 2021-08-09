from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models


class UserCreateFrom(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name' , 'last_name', )
