from django.db import models
from users.models import User,Organizer,Client
from events.models import Event,EventCategory,TicketType

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status_choices = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking #{self.booking_id} - {self.client.username}"
    
class BookingTicketInfo(models.Model):
    
    id = models.AutoField(primary_key=True)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking Ticket Info #{self.id} - {self.ticket_type.name}"