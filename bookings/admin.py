from django.contrib import admin
from .models import TicketType, Booking, BookingTicketInfo

# Register your models here.
admin.site.register(TicketType)
admin.site.register(Booking)
admin.site.register(BookingTicketInfo)