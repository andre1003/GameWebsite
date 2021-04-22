from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('singup/', SingUpView.as_view(), name='singup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/<str:token>/', LoginByTokenView.as_view(), name="login_by_token"),
    path('data/', GetDataView.as_view(), name='data'),
    path('data/edit/', EditDataView.as_view(), name="edit_data"),
    path('feedback/<str:username>', Feedback.as_view(), name='feedback'),
    path('search/', Search.as_view(), name="search")
]