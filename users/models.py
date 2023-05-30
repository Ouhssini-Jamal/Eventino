from django.contrib.auth.models import AbstractUser
from django.db import models
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
    
    # Additional fields and methods specific to the Client model

