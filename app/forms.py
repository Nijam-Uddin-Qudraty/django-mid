from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .import models


class Register_form(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class Update(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class CarForm(forms.ModelForm):
    class Meta:
        model = models.Car
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields= ['name','email','body']
