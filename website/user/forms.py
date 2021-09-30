from django import forms
from django.forms import TextInput, PasswordInput, widgets
from django.forms.fields import CharField, EmailField, IntegerField
from .models import Decision, Group, Match, Player
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    first_name = CharField(max_length=30, help_text='Required', widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira seu nome'}))
    last_name = CharField(max_length=30, help_text='Required', widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira seu sobrenome'}))
    email = forms.EmailField(max_length=254, help_text='Required', widget=widgets.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Insira um e-mail'}))
    username = CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira um nome de usuário'}))
    password1 = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'id': 'password1', 'placeholder': 'Insira uma senha'}))
    password2 = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'id': 'password2', 'placeholder': 'Confirme a senha'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        '''
        :Params:
            self, *args, **kwargs
        :Return:
            Initiate the attributes correctly
        :Description:
            Remove autofocus on username
        '''
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)


class PlayerRegisterForm(forms.ModelForm):
    age = IntegerField(help_text='Required', widget=widgets.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Insira sua idade'}))
    
    class Meta:
        model = Player
        fields = ['age']


class LoginForm(forms.ModelForm):
    '''
    :Type:
        Login form
    :Attributes:
        username, password
    :Description:
        Form for authenticate an user
    '''
    
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(
                attrs={
                    'class': 'login-form-control',
                    'placeholder': 'Insira o nome de usuário',
                }
            ),
            'password': PasswordInput(
                attrs={
                    'class': 'login-form-control',
                    'placeholder': 'Insira sua senha',
                }
            ),
        }


class MatchRegisterForm(forms.ModelForm):
    group = forms.CharField(max_length=254, help_text='Required')
    
    class Meta:
        model = Match
        fields = ['role', 'hits', 'mistakes', 'individual_feedback']


class DecisionRegisterForm(forms.ModelForm):
    class Meta:
        model = Decision
        fields = ['decision', 'scenery', 'is_mistake']


class GroupRegisterForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'score']

class FeedbackForm(forms.Form):
    def __init__(self, date, individual_feedback, hits, mistakes, *args, **kwargs):
        self.date = date
        self.individual_feedback = individual_feedback
        self.hits = hits
        self.mistakes = mistakes
        super(FeedbackForm, self).__init__(*args, **kwargs)
