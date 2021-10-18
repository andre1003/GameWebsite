from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse, response
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Coalesce
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from .forms import *
from .models import *


# Views

class HomeView(View):
    template_name = 'user/home.html'

    def get(self, request, *args, **kwargs):
        print(self.request.META)
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

            user = authenticate(username=user_form['username'].value(), password=user_form['password1'].value())
            login(request, user)

            messages.success(request, 'Conta criada com sucesso!')
            return redirect('home')

        else:
            messages.error(request, 'Houve um erro ao criar a conta.')
            return redirect('home')


class LoginView(View):
    template_name = 'user/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        form = {
            'form': self.form_class()
        }

        return render(request, self.template_name, form)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user = authenticate(username=form['username'].value(), password=form['password'].value())
        
        if user is not None:
            messages.success(request, f'Usuário autenticado com sucesso!')
            login(request, user)

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))

            else:
                return redirect('home')
        else:
            messages.error(request, f'Erro ao autenticar usuário, tente novamente!')
            return redirect('login')


@method_decorator(csrf_exempt, name="dispatch")
class GameLoginView(View):
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request=request, data = request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            login(request, user)

            data = {
                'response': 'success'
            }

            return JsonResponse(data)
        
        else:
            data = {
                'response': 'fail'
            }
            return JsonResponse(data)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


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
        messages.success(request, 'Dados alterados com sucesso!')
        if user_form['password1'].value():
            user.set_password(user_form['password1'].value())
            user.save()

        return redirect('home')


class SearchView(LoginRequiredMixin, View):
    template_name = 'user/search.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_staff:
            return render(request, self.template_name, {'player': None})
        else:
            messages.error(request, f"Você não tem permissão para acessar essa página!")
            return redirect('home')
        # matchs = Match.objects.filter(player=user.player)
        # hits = 0
        # mistakes = 0

        # for match in matchs:
        #     hits += match.hits
        #     mistakes += match.mistakes

        # return render(request, self.template_name, {'matchs': matchs, 'hits': hits, 'mistakes': mistakes})
    
    def post(self, request, *args, **kwargs):
        name = request.POST['search']
        all_users = User.objects.annotate(fullname=Concat('first_name', Value(' '), 'last_name')).filter(Q(fullname__icontains=name))
        users = list()
        
        if not all_users:
            messages.error(request, f"Nenhum aluno encontrado!")
            return render(request, self.template_name, {'users': users})

        else:
            for user in all_users:
                try:
                    match = Match.objects.filter(player=user.player)
                    if match:
                        users.append(user)
                
                except:
                    pass
            
            if not users:
                messages.error(request, f'O aluno que você procura não possui um feedback cadastrado!')
            return render(request, self.template_name, {'users': users})


class FeedbackView(LoginRequiredMixin, View):
    template_name = 'user/feedback.html'
    form_class = FeedbackForm

    def get(self, request, username, *args, **kwargs):
        if request.user.is_staff:
            user = User.objects.get(username=username)

            matchs = Match.objects.filter(player=user.player)

            feedbacks = list()
            
            for match in matchs:
                month = str(match.created_at.month).zfill(2)
                day = str(match.created_at.day).zfill(2)
                date = f"{day}/{month}/{match.created_at.year}"
                if match.role == 'Scrum Master' or match.role == 'Product Owner' or match.role == 'Time de Desenvolvimento':
                    method = 'Scrum'
                else:
                    method = 'eXtreme Programming'

                form = self.form_class(date, match.individual_feedback, match.hits, match.mistakes, match.match_id, match.role, method)

                feedbacks.append(form)

            return render(request, self.template_name, {'feedbacks': feedbacks})

        else:
            messages.error(request, f"Você não tem permissão para acessar essa página!")
            return redirect('home')

    def post(self, request, *args, **kwargs):
        return redirect('search')


class DecisionsView(LoginRequiredMixin, View):
    template_name = 'user/decisions.html'
    
    def get(self, request, match_id, *args, **kwargs):
        if request.user.is_staff:
            try:
                match = Match.objects.get(match_id=match_id)
                decisions = Decision.objects.filter(match=match)

                return render(request, self.template_name, {'decisions': decisions})

            except:
                messages.warning(request, 'Partida não encontrada!')
                return redirect('search')

        else:
            messages.error(request, 'Você não tem permissão para acessar essa página!')
            return redirect('home')

    def post(self, request, match_id, *args, **kwargs):
        match = Match.objects.get(match_id=match_id)
        return redirect(f'feedback', match.player.user)


@method_decorator(csrf_exempt, name="dispatch") # This is for disable csrf token
class MatchRegisterView(LoginRequiredMixin, View):
    form_class = MatchRegisterForm
    template_name = 'user/tests.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        user = request.user

        match_form = self.form_class(request.POST)

        if match_form.is_valid():
            match_form.instance.player = user.player

            group = Group.objects.get(name=match_form['group'].value())
            match_form.instance.group = group
            
            print(f'\n\n{group.name} - Score: {group.score}')

            match = match_form.save()
            
            group.score += match.hits
            group.save()

            """
            The following code just get the match saved and returns the match_id in
            a JSON response. This is important for saving multiple decisions,
            following the order:

            Save a match (it returns match_id) > Save n decisions, with the match_id
            """
            data = {
                'response': match.match_id
            }

            return JsonResponse(data)


@method_decorator(csrf_exempt, name="dispatch") # This is for disable csrf token
class DecisionRegisterView(View):
    form_class = DecisionRegisterForm

    def post(self, request, match_id, *args, **kwargs):
        decision_form = self.form_class(request.POST)

        if decision_form.is_valid():
            match = Match.objects.get(match_id=match_id)

            decision_form.instance.match = match
            decision_form.save()

        return HttpResponse("Done")


@method_decorator(csrf_exempt, name="dispatch") # This is for disable csrf token
class GroupRegisterView(View):
    form_class = GroupRegisterForm

    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            obj, created = Group.objects.get_or_create(name=form['name'].value(), defaults={'score': 0})

        return HttpResponse("Done")


class RankingView(View):
    template_name = 'user/ranking.html'

    def get(self, request, *args, **kwargs):
        
        groups = Group.objects.order_by('-score')
        position = 1

        ranking = list()
        for group in groups:
            ranking.append({'name': group.name, 'score': group.score, 'position': position})
            position+=1

        return render(request, self.template_name, {'ranking': ranking})




# Error handler
class Handler404(TemplateView):
    template_name = 'errors/404.html'

    @classmethod
    def get_rendered_view(cls):
        as_view_fn = cls.as_view()

        def view_fn(request):
            response = as_view_fn(request)
            response.render()
            response.status_code = 404
            return response

        return view_fn
