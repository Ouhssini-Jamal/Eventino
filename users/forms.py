# forms.py
from django import forms
from datetime import date, timedelta
from users.models import Organizer, Client ,User
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth import authenticate

class OrganizerForm(forms.ModelForm):

    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    phone_number = forms.CharField(validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Invalid phone number.")])
    email = forms.CharField(validators=[EmailValidator(message="Invalid email address.")])

    
    class Meta:
        model = Organizer
        fields = ['username', 'email', 'password', 'confirm_password', 'phone_number', 'description', 'image', 'social_media_link']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control form-control-xl'
        self.fields['username'].widget.attrs['placeholder'] = 'Organization name'
        self.fields['email'].widget.attrs['class'] = 'form-control form-control-xl'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password'].widget.attrs['class'] = 'form-control form-control-xl'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['confirm_password'].widget.attrs['class'] = 'form-control form-control-xl'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control form-control-xl'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone Number'
        self.fields['description'].widget.attrs['class'] = 'form-control form-control-xl'
        self.fields['description'].widget.attrs['placeholder'] = 'Description'
        self.fields['image'].widget.attrs['class'] = 'form-control form-control-xl'
        self.fields['social_media_link'].widget.attrs['class'] = 'form-control form-control-xl'
        self.fields['social_media_link'].widget.attrs['placeholder'] = 'Social Media Link'


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
    phone_number = forms.CharField(validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Invalid phone number.")])
    email = forms.CharField(validators=[EmailValidator(message="Invalid email address.")])
    first_name = forms.CharField(validators=[RegexValidator(r'^[a-zA-Z\s]*$', message="Invalid first name.")])
    last_name = forms.CharField(validators=[RegexValidator(r'^[a-zA-Z\s]*$', message="Invalid last name.")])
    
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Client
        fields = ['username', 'first_name', 'last_name','cin','email', 'password', 'confirm_password', 'birthdate', 'phone_number', 'image']

        widgets = {
            'password': forms.PasswordInput(),
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control form-control-xl'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['first_name'].widget.attrs['class'] = 'form-control form-control-xl'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control form-control-xl'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'].widget.attrs['class'] = 'form-control form-control-xl'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password'].widget.attrs['class'] = 'form-control form-control-xl'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['confirm_password'].widget.attrs['class'] = 'form-control form-control-xl'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['birthdate'].widget.attrs['class'] = 'form-control form-control-xl'
        self.fields['birthdate'].widget.attrs['placeholder'] = 'Birthdate'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control form-control-xl'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone Number'
        self.fields['cin'].widget.attrs['class'] = 'form-control form-control-xl'
        self.fields['cin'].widget.attrs['placeholder'] = 'Cin'
        self.fields['image'].widget.attrs['class'] = 'form-control form-control-xl'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')
        birthdate = cleaned_data.get('birthdate')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        if email and Organizer.objects.filter(email=email).exists():
            self.add_error('email', "Email address already exists")

        if phone_number and Organizer.objects.filter(phone_number=phone_number).exists():
            self.add_error('phone_number', "Phone number already exists")

        if birthdate and (date.today() - birthdate) < timedelta(days=365*18):
            self.add_error('birthdate', "Must be at least 18 years old")

        return cleaned_data
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data
