from django.shortcuts import render
from .forms import EventForm,EventUpdateForm
from .models import Event,Category,EventCategory
# Create your views here.

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
        'form' : EventForm(),
        'form1' : EventUpdateForm(),
         }

            return render(request, 'manage_event_org.html',context)  # Redirect to event detail page
    else:
        context = {
            'events': events,
            'form' : EventForm(),
            'form1' : EventUpdateForm(),
         }
        return render(request, 'manage_event_org.html',context )
    
def index1(request):
    events = Event.objects.filter(organizer_id=request.user.id)
    context = {
        'events': events,
        'form'  : EventForm(),
        'form1' : EventUpdateForm(),
        }
    return render(request, 'manage_event_org.html',context) 

def index2(request):
    pending_events = Event.objects.filter(status='pending')
    other_events = Event.objects.exclude(status='pending')
    events = list(pending_events) + list(other_events)
    context = {
        'events': events,
        }
    return render(request, 'manage_event_adm.html',context)
 
def validate_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.status == 'pending':
        event.status = 'confirmed'
        event.save()
    return redirect('events:manage_adm')

from django.shortcuts import render, get_object_or_404, redirect
import logging
    
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        form = EventUpdateForm(request.POST, instance=event)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            for field in form.fields:
                value = cleaned_data.get(field)
                if value is not None:
                    setattr(event, field, value)
            # dd(event)
            event.save()
            return redirect('events:create')
    
def event_detail(request, event_id):
    event = get_object_or_404(Event, event_id=event_id)
    return render(request, 'event_detail.html', {'event': event})
 
def event_listing(request) :
    context = {
         'categories' : Category.objects.all(),
     }
    return render(request,'event_listing.html',context)
