from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *


# Views

class HomeView(View):
    template_name = 'user/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SingUpView(View):
    template_name = 'user/singup.html'
    form_class = (PlayerRegisterForm, UserRegisterForm)

    def get(self, request, *args, **kwargs):
        forms = {
            'player_form': self.form_class[0](),
            'user_form': self.form_class[1]()
        }

        return render(request, self.template_name, forms)

    def post(self, request, *args, **kwargs):
        player_form = self.form_class[0](request.POST)
        user_form = self.form_class[1](request.POST)

        if player_form.is_valid() and user_form.is_valid():
            user_form.save()
            player_form.instance.user = User.objects.get(username=user_form['username'].value())
            player_form.save()

            messages.success(request, 'Conta criada com sucesso!')
            return redirect('home')

        else:
            messages.error(request, 'Houve um erro ao criar a conta.')
            return redirect('home')


class LoginView(View):
    template_name = 'user/login.html'
    form_class = AuthenticationForm

    def get(self, request, *args, **kwargs):
        form = {
            'form': self.form_class()
        }

        return render(request, self.template_name, form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            login(request, user)

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))

            else:
                return redirect('home')

        else:
            return HttpResponse(500)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class LoginByTokenView(View):
    def get(self, request, token, *args, **kwargs):
        player = Player.objects.get(auth_token=token)
        login(request, player.user)

        data = {
            'username': player.user.username,
            'age': player.age,
            'auth_token': player.auth_token
        }

        return JsonResponse(data)


class GetDataView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user

        matchs = Match.objects.filter(player=user.player)
        hits = 0
        mistakes = 0

        for match in matchs:
            hits += match.hits
            mistakes += match.mistakes

        data = {
            'username': user.username,
            'hits': hits,
            'mistakes': mistakes,
            'auth_token': user.player.auth_token
        }

        return JsonResponse(data)


class EditDataView(LoginRequiredMixin, View): # PRECISA REALIZAR O POST E REVISAR
    template_name = 'user/data.html'
    form_class = UserRegisterForm

    def get(self, request, *args, **kwargs):
        user = request.user

        data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email, 
            'password1': user.password,
            'password2': user.password
        }

        forms = {
            'user_form': self.form_class(data, auto_id=False),
            'user': user
        }

        return render(request, self.template_name, forms)

    def post(self, request, *args, **kwargs):
        user = request.user

        user_form = self.form_class(request.POST)

        update_list = list()

        if user_form['username'].value() != user.username:
            user.username = user_form['username'].value() 
            update_list.append('username')

        if user_form['first_name'].value()  != user.first_name:
            user.first_name = user_form['first_name'].value() 
            update_list.append('first_name')

        if user_form['last_name'].value()  != user.last_name:
            user.last_name = user_form['last_name'].value() 
            update_list.append('last_name')
        
        if user_form['email'].value()  != user.email:
            user.email = user_form['email'].value() 
            update_list.append('email')

        user.save(update_fields=update_list)
        return redirect('home')


class Test(View):
    template_name = 'user/test.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        matchs = Match.objects.filter(player=user.player)
        hits = 0
        mistakes = 0

        for match in matchs:
            hits += match.hits
            mistakes += match.mistakes

        return render(request, self.template_name, {'matchs': matchs, 'hits': hits, 'mistakes': mistakes})