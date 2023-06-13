from django.contrib import admin
from .models import User, Organizer, Client

# Register your models here.
admin.site.register(User)
admin.site.register(Organizer)
admin.site.register(Client)
