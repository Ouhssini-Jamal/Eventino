from django.urls import path
from . import views
# from .views import OrganizerRegistrationView, ClientRegistrationView
from django.contrib.auth.decorators import login_required
app_name = 'bookings'


urlpatterns = [
  path('event/<int:event_id>/book/', login_required(views.EventBooking), name='event_booking'),
path('event/<int:event_id>/', login_required(views.show_bookings), name='show_bookings'),
  path('client/', login_required(views.client_bookings), name='client_bookings'),
]

