# forms.py
from django import forms
import re
from users.models import Organizer, Client
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core.validators import EmailValidator, RegexValidator

class OrganizerForm(forms.ModelForm):

    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    phone_number = forms.CharField(validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Invalid phone number.")])
    email = forms.CharField(validators=[EmailValidator(message="Invalid email address.")])
    first_name = forms.CharField(validators=[RegexValidator(r'^[a-zA-Z\s]*$', message="Invalid first name.")])
    last_name = forms.CharField(validators=[RegexValidator(r'^[a-zA-Z\s]*$', message="Invalid last name.")])

    class Meta:
        model = Organizer
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'phone_number', 'description', 'image', 'social_media_link']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        if email and Organizer.objects.filter(email=email).exists():
            self.add_error('email', "Email address already exists")

        if phone_number and Organizer.objects.filter(phone_number=phone_number).exists():
            self.add_error('phone_number', "Phone number already exists")
        return cleaned_data

class ClientForm(forms.ModelForm):
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    class Meta:
        model = Client
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'birthdate', 'phone_number', 'image']
        widgets = {
            'password': forms.PasswordInput(),
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        return cleaned_data
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))