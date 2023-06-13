from django.shortcuts import render
from .forms import EventForm
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
         }

            return render(request, 'add_event.html',context)  # Redirect to event detail page
    else:
        context = {
            'events': events,
            'form' : EventForm(),
         }
        return render(request, 'add_event.html',context )