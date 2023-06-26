from django.db import models
from users.models import User,Organizer,Client

# Create your models here.
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='EventCategory')
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_datetime = models.DateTimeField(null=True,blank=True)
    end_datetime = models.DateTimeField(null=True,blank=True)
    quantity_left = models.PositiveIntegerField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images/')
    standard = models.DecimalField(null=True,max_digits=8, decimal_places=2)
    mid = models.DecimalField(null=True,max_digits=8, decimal_places=2) 
    vip = models.DecimalField(null=True,max_digits=8, decimal_places=2)  
    standard_left = models.PositiveIntegerField(null=True)
    mid_left = models.PositiveIntegerField(null=True) 
    vip_left = models.PositiveIntegerField(null=True) # Add price field here
    status_choices = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('finished', 'Finished'),
    ]
    status = models.CharField(max_length=50, choices=status_choices, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def calculate_total_price(self, quantities):
        ticket_prices = {
            'standard': self.standard,
            'mid': self.mid,
            'vip': self.vip
        }
      
        total_price = 0
        for ticket_type, quantity in quantities.items():
            if quantity > 0 and ticket_type in ticket_prices:
                ticket_price = ticket_prices[ticket_type]
                total_price += ticket_price * quantity

        return total_price
    def update_event_fields(event, fields):
        for field_name, field_value in fields.items():
            if hasattr(event, field_name):
                setattr(event, field_name, field_value)
        event.save()
    # @property
    # def msg():
    #     return ""
    
class EventCategory(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Event: {self.event.name}, Category: {self.category.name}"
    
