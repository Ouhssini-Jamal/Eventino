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
# path('search/', views.event_search, name='event_search'),
path('search/', views.search_events, name='search_events'),
path('clients/admin/', login_required(views.manage_clients), name='manage_clients'),
path('organizers/admin/', login_required(views.manage_organizers), name='manage_organizers'),
path('validate_organizer/<int:id>/', login_required(views.validate_organizer), name='validate_organizer'),
path('profile/admin/', login_required(views.admin_profile), name='admin_profile'),
path('organizer/profile/', login_required(views.organizer_profile), name='organizer_profile'),
path('client/profile/',login_required(views.client_profile), name='client_profile'),


]

