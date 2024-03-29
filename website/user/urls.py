from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('singup/', SingUpView.as_view(), name='singup'),
    path('login/', LoginView.as_view(), name='login'),
    path('game-login/', GameLoginView.as_view(), name="game_login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('data/edit/', EditDataView.as_view(), name="edit_data"),
    path('feedback/<str:username>', FeedbackView.as_view(), name='feedback'),
    path('decisions/<str:match_id>', DecisionsView.as_view(), name='decision_view'),
    path('search/', SearchView.as_view(), name="search"),
    path('match-register/', MatchRegisterView.as_view(), name="match_register"),
    path('decision-register/<str:match_id>/', DecisionRegisterView.as_view(), name="decision_register"),
    path('group-register/', GroupRegisterView.as_view(), name="group_register"),
    path('ranking/', RankingView.as_view(), name="ranking"),
]