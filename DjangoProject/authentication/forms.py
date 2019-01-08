from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser
import re


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = MyUser
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")


class SetPasswordForm(forms.Form):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmation', widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if len(password1) < 8:
            raise forms.ValidationError('Passsword must be atleat 8 characters.')
        if not re.search("[0-9]", password1):
            raise forms.ValidationError('Passsword must have atleast 1 digit.')
        if not re.search("[a-z]", password1):
            raise forms.ValidationError('Passsword must have combination of lowercase and uppercase.')
        if not re.search("[A-Z]", password1):
            raise forms.ValidationError('Passsword must have combination of lowercase and uppercase.')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data['password2']
        if password2 != password1:
            raise forms.ValidationError('Passsword must match')
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
