# urls.py
from django.urls import path
from . import views
# from .views import OrganizerRegistrationView, ClientRegistrationView
from django.contrib.auth.decorators import login_required


urlpatterns = [
path('', views.index, name= 'index'),
path('login/', views.login_view, name='login_view'),
path('register/', views.register_view, name='register'),
path('registerclient/', views.register_client, name='registercli'),
path('registerorg/', views.register_organizer, name='registerorg'),
path('homepage/', login_required(views.home), name='home'),
 path('logout/', views.logout_view, name='logout'),
]

