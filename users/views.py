# views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import OrganizerForm, ClientForm,LoginForm
from .models import Client, Organizer, User
from django.contrib.auth import logout
from django.http import HttpResponseForbidden




def register_organizer(request):
    organizer_form = OrganizerForm(request.POST, request.FILES)
    if request.method == 'POST':
        if organizer_form.is_valid():
            user = organizer_form.save(commit=False)
            user.set_password(organizer_form.cleaned_data['password'])
            # user.is_active = False  # Set the is_active flag to True
            user.save()
            return redirect('login_view')   # Redirect to the desired page after successful registration
        else : 
            context = {
        'organizer_form': organizer_form
    }
            return render(request, 'register_organizer.html',context)
    else:
          organizer_form = OrganizerForm()
    context = {
        'organizer_form': organizer_form
    }
    return render(request, 'register_organizer.html', context)
        

def register_client(request):
    form = ClientForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login_view')  # Redirect to the desired page after successful registration
        else : 
            context = {
         'client_form': form,
    }
            return render(request, 'register_client.html',context)
    else:
        client_form = ClientForm() 
    context = {
        'client_form': client_form
    }
    return render(request, 'register_client.html', context)

def login_view(request):
    form = LoginForm(request, data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dash')    
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

def dashboard_show(request):
    user = request.user
    if hasattr(user, 'organizer'):
        return render(request, 'Dashboard-organizer.html')
    elif hasattr(user, 'client'):
         return render(request, 'Dashboard-client.html')


def index(request):
     return render(request,'index.html')
