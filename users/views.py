# views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import OrganizerForm, ClientForm,LoginForm
from .models import Client, Organizer, User 
from bookings.models import Booking
from events.models import Event,EventCategory,Category
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
from django.db.models import Sum

def dashboard_show(request):
    user = request.user
    if hasattr(user, 'organizer'):
        event_count = user.event_set.count()
        events = Event.objects.filter(organizer=user)
        confirmed_bookings = Booking.objects.filter(event__in=events, status='confirmed')
        total_earnings = confirmed_bookings.aggregate(Sum('total_price'))['total_price__sum']
        if total_earnings is None : total_earnings = 0
        total_bookings = confirmed_bookings.count()
        context = {'event_count': event_count,
                   'total_earnings': total_earnings,
                   'total_bookings' : total_bookings
                   }
        return render(request, 'Dashboard-organizer.html',context)
    elif hasattr(user, 'client'):
        bk = Booking.objects.filter(client=user, status='confirmed')
        total_bookings = bk.count()
        total_spending = bk.aggregate(sum_total=Sum('total_price'))
        total_spending = total_spending['sum_total'] or 0
        context = {'total_bookings': total_bookings,
                   'total_spending': total_spending,
                   }
        return render(request, 'Dashboard-client.html',context)
    elif user.is_superuser: 
        context = {
        'total_events_count': Event.objects.count(),
        'total_organizers_count': Organizer.objects.count(),
        'total_clients_count': Client.objects.count(),
        }
        return render(request, 'Dashboard-admin.html',context)


def index(request):
     categories = Category.objects.all()
     context = {'categories': categories}
     return render(request,'index.html',context)

# def event_search(request):
#     query = request.GET.get('EventName', '')  # Get the search query from the request GET parameters
#     events = Event.objects.filter(
#         Q(name__icontains=query) |        # Search by event name (case-insensitive)
#         Q(location__icontains=query)   # Search by city (case-insensitive)
#     ).filter(status="confirmed").distinct()
#     context = {
#         'query': query,
#         'events': events,
#         'categories' : Category.objects.all(),
#     }

def search_events(request):
    query = request.GET.get('EventName', '')  # Get the search query from the request GET parameters
    events = Event.objects.all()
    if query :
        events = events.filter(
            Q(name__icontains=query) |        # Search by event name (case-insensitive)
            Q(location__icontains=query)   # Search by city (case-insensitive)
        ).filter(status="confirmed").distinct()
    category_id = request.GET.get('category')
    if category_id:
        category = Category.objects.get(category_id=category_id)
        events = events.filter(categories=category, status='confirmed')
    Date = request.GET.get('Date')

    if Date : 
        events = events.filter(start_datetime__date=Date)
    
    Price = request.GET.get('Price')
    if Price:
        events = events.filter(standard__lte=Price, status='confirmed')
        
    categories = Category.objects.all()
    context = {
        'categories' :categories,
        'events': events,
    }
    return render(request,'event_listing.html',context)

def manage_clients(request):
    clients = Client.objects.all()
    return render(request, 'manage_clients.html', {'clients': clients})

def manage_organizers(request):
    organizers = Organizer.objects.all()
    for organizer in organizers:
        event_count = organizer.event_set.count()
        organizer.event_count = event_count
    return render(request, 'manage_organizers.html', {'organizers': organizers})


def validate_organizer(request, id):
    organizer = Organizer.objects.get(id=id)
        # Perform validation logic here
    organizer.is_active = True
    organizer.save()
        # Redirect to a success page or a different URL
    return redirect('manage_organizers')

def admin_profile(request):
    return render(request, 'admin_profile.html')

def organizer_profile(request):
    return render(request, 'organizer_profile.html')

def client_profile(request):
    return render(request, 'client_profile.html')