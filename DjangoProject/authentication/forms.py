from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import MyUser


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = MyUser
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")
