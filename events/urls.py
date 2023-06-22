from django.urls import include,path
from . import views
# from .views import OrganizerRegistrationView, ClientRegistrationView
from django.contrib.auth.decorators import login_required
app_name = 'events'


urlpatterns = [
    path('organizer', login_required(views.index1), name='manage_org'),
    path('admin', login_required(views.index2), name='manage_adm'),
    path('create/', login_required(views.create_event), name='create'),
    path('update/<int:event_id>/', login_required(views.update_event), name='update_event'),
    path('<int:event_id>/', login_required(views.event_detail), name='event_detail'),
    path('event/validate/<int:event_id>/', login_required(views.validate_event), name='validate_event'),
]

