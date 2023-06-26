from django.contrib.auth.models import AbstractUser
from django.db import models
# from event.models import Event,EventCategory,Category
# Create your models here.
# models.py
class User(AbstractUser) :
    pass
class Organizer(User):
    phone_number = models.CharField(max_length=20)
    description = models.TextField()
    image = models.ImageField(upload_to='organizer_images/')
    social_media_link = models.URLField(blank=True)

    # Additional fields and methods specific to the Organizer model

class Client(User):
    birthdate = models.DateField()
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='client_images/')
    cin = models.CharField(max_length=20)
    @property
    def is_client(self):
        return True
    # Additional fields and methods specific to the Client model
    
# class TicketType(models.Model):
#     TicketType_id = models.AutoField(primary_key=True)
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     quantity = models.PositiveIntegerField()
#     reated_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

# class Booking(models.Model):
#     booking_id = models.AutoField(primary_key=True)
#     client = models.ForeignKey(User, on_delete=models.CASCADE)
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)
#     total_price = models.DecimalField(max_digits=8, decimal_places=2)
#     status_choices = [
#         ('pending', 'Pending'),
#         ('confirmed', 'Confirmed'),
#         ('cancelled', 'Cancelled'),
#     ]
#     status = models.CharField(max_length=20, choices=status_choices, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Booking #{self.booking_id} - {self.client.username}"
    
# class BookingTicketInfo(models.Model):
    
#     id = models.AutoField(primary_key=True)
#     ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
#     booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Booking Ticket Info #{self.id} - {self.ticket_type.name}"