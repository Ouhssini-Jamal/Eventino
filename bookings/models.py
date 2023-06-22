from django.db import models
from users.models import User,Organizer,Client
from events.models import Event,EventCategory

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
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

class TicketBookingType(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.ticket_type} - {self.booking}"