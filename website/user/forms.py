from django import forms
from django.forms import TextInput, PasswordInput
from .models import Decision, Match, Player
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='Required')
    last_name = forms.CharField(max_length=30, help_text='Required')
    email = forms.EmailField(max_length=254, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class PlayerRegisterForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['age']
        # widgets = {
        #     'age': TextInput(
        #         attrs={
        #             'placeholder': 'Insira sua idade'
        #         }
        #     )
        # }


class MatchRegisterForm(forms.ModelForm):
    group = forms.CharField(max_length=254, help_text='Required')
    
    class Meta:
        model = Match
        fields = ['role', 'hits', 'mistakes', 'individual_feedback']


class DecisionRegisterForm(forms.ModelForm):
    class Meta:
        model = Decision
        fields = ['decision', 'scenery', 'is_mistake']