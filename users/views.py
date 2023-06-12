# views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import OrganizerForm, ClientForm,LoginForm,EventForm
from .models import Client, Organizer, User ,Event,EventCategory
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from django.db.models import Q


def register_organizer(request):
    user = request.user
    if user.is_authenticated:
        return redirect('dash')
    else:
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
    user = request.user
    if user.is_authenticated:
        return redirect('dash')
    else:
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
    user = request.user
    if user.is_authenticated:
        return redirect('dash')
    else :
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

def event_search(request):
    query = request.GET.get('q', '')  # Get the search query from the request GET parameters
    events = Event.objects.filter(
        Q(name__icontains=query) |        # Search by event name (case-insensitive)
        Q(location__icontains=query) |   # Search by city (case-insensitive)
        Q(categories__name__icontains=query)   # Search by category name (case-insensitive)
    ).exclude(status='pending').distinct()
    context = {
        'query': query,
        'events': events,
    }

    return render(request, 'index.html', context)

def create_event(request):
    events = Event.objects.filter(organizer_id=request.user.id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer_id = request.user.id  # Set the organizer_id to the current user's id
            event.save()
            categories = form.cleaned_data['categories']  # Get the selected categories from the form
            for category in categories:
                event.categories.add(category)
            context = {
        'events': events,
         }

            return render(request, 'add_event.html',context)  # Redirect to event detail page
    else:
        context = {
            'events': events,
            'form' : EventForm(),
         }
        return render(request, 'add_event.html',context )
