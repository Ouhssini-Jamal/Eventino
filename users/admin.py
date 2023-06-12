from django.contrib import admin
from .models import User, Organizer, Client , Event , Category , EventCategory ,TicketType , BookingTicketInfo,Booking
# Register your models here.
admin.site.register(User)
admin.site.register(Organizer)
admin.site.register(Event)
admin.site.register(Category)
admin.site.register(EventCategory)
admin.site.register(TicketType)
admin.site.register(Booking)
admin.site.register(BookingTicketInfo)