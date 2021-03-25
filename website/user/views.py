from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *


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

        data = {
            'username': user.username,
            'age': user.player.age,
            'auth_token': user.player.auth_token
        }

        return JsonResponse(data)