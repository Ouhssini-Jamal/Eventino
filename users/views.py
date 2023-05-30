# views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import OrganizerForm, ClientForm,LoginForm
from .models import Client, Organizer, User
from django.contrib.auth import logout



def register_organizer(request):
    organizer_form = OrganizerForm(request.POST, request.FILES)
    if request.method == 'POST':
        if organizer_form.is_valid():
            user = organizer_form.save(commit=False)
            user.set_password(organizer_form.cleaned_data['password'])
            # user.is_active = False  # Set the is_active flag to True
            user.save()
            login(request, user)
            return redirect('home')  # Redirect to the desired page after successful registration
        else : 
            client_form = ClientForm()
            context = {
         'client_form': client_form,
        'organizer_form': organizer_form
    }
            return render(request, 'register.html',context)
        
    

def register_client(request):
    form = ClientForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')  # Redirect to the desired page after successful registration
        else : 
            organizer_form = OrganizerForm
            context = {
         'client_form': form,
        'organizer_form': organizer_form
    }
            return render(request, 'register.html',context)


def login_view(request):
    form = LoginForm(request, data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if hasattr(user, 'organizer'):
                    return redirect('home')  # Redirect to home page for organizers
                elif hasattr(user, 'client'):
                    return  redirect('home')# Redirect to home page for clients
        else:
            context = {
                'form': form,
            }
            return render(request, 'login.html', context)
    else :
        f = LoginForm()
        return render(request, 'login.html', {'form': f})

def logout_view(request):
    logout(request)
    return redirect('index')  # Replace 'home' with the URL or name of your desired homepage

def home(request):
    return render(request,'home.html')

def register_view(request):
    client_form = ClientForm()
    organizer_form = OrganizerForm()
    context = {
        'client_form': client_form,
        'organizer_form': organizer_form
    }
    return render(request, 'register.html', context)


def index(request):
     return render(request,'index.html')