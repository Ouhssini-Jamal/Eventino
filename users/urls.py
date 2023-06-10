# urls.py
from django.urls import path
from . import views
# from .views import OrganizerRegistrationView, ClientRegistrationView
from django.contrib.auth.decorators import login_required


urlpatterns = [
path('', views.index, name= 'index'),
path('login/', views.login_view, name='login_view'),
path('register_client/', views.register_client, name='registercli'),
path('register_organizer/', views.register_organizer, name='registerorg'),
path('Dashboard/', login_required(views.dashboard_show), name='dash'),
path('logout/', views.logout_view, name='logout'),
]

