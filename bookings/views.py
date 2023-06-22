from django.shortcuts import render,redirect,get_object_or_404
from events.models import Event
from .models import Booking,TicketBookingType
from django.db.models import F

# Create your views here.
def EventBooking(request,event_id) :
    event = Event.objects.get(pk=event_id)
    quantities = {
                'standard': int(request.POST.get('standard_quantity')),
                'mid': int(request.POST.get('mid_quantity')),
                'vip': int(request.POST.get('vip_quantity'))
            }
    total_quantity = sum(quantities.values())
    if total_quantity <= event.quantity_left:
                # Update the quantity_left field
            event.quantity_left = F('quantity_left') - total_quantity
            event.save()
            
            event = Event.objects.get(pk=event_id)
            booking = Booking.objects.create(
                    event=event,
                    client=request.user,
                    quantity=total_quantity,
                    total_price=event.calculate_total_price(quantities),
                )
                 # Create TicketBookingType instances for each ticket type
            for ticket_type, quantity in quantities.items():
                 if quantity > 0:
                    TicketBookingType.objects.create(
                    booking=booking,
                     ticket_type=ticket_type,
                    quantity=quantity
             )
            return redirect('events:event_detail', event_id=event.event_id)
    else :  
        context ={
            'msg' : 'vous avez depasser le nombres de tickets',
            'event': event,
        }
        return render(request, 'event_detail.html', context)
    
def show_bookings(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    bookings = Booking.objects.filter(event=event).order_by('-status')
    context = {
        'event': event,
        'bookings': bookings,
    }
    return render(request, 'event_bookings.html', context)