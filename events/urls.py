from django.urls import path
from . import views
# from .views import OrganizerRegistrationView, ClientRegistrationView
from django.contrib.auth.decorators import login_required
app_name = 'events'


urlpatterns = [
    path('add_event/', login_required(views.create_event), name='add_event')
]

