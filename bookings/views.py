from django.shortcuts import render,redirect,get_object_or_404
from events.models import Event
from .models import Booking,TicketBookingType
from django.db.models import F
from django.contrib import messages

# Create your views here.
def EventBooking(request,event_id) :
    event = Event.objects.get(pk=event_id)
    quantities = {
                'standard': int(request.POST.get('standard_quantity')),
                'mid': int(request.POST.get('mid_quantity')),
                'vip': int(request.POST.get('vip_quantity'))
            }
    if quantities['standard'] > event.standard_left or quantities['mid'] > event.mid_left or quantities['vip'] > event.vip_left :
        messages.error(request, 'You have exceeded the number of tickets')
        return redirect('events:event_detail', event_id=event.event_id)

    else :
            total_quantity = sum(quantities.values())
                # Update the quantity_left field
            event.quantity_left = F('quantity_left') - total_quantity
            event.standard_left -= quantities['standard']
            event.standard_left -= quantities['mid'] 
            quantities['vip'] -= event.vip_left 
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
            return redirect('bookings:client_bookings')
    
def show_bookings(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    bookings = Booking.objects.filter(event=event).order_by('-status')
    context = {
        'event': event,
        'bookings': bookings,
    }
    return render(request, 'event_bookings.html', context)

def client_bookings(request):
    # Retrieve bookings for the client
    bookings = Booking.objects.filter(client=request.user)

    # Retrieve booking ticket types for each booking
    booking_ticket_types = []
    for booking in bookings:
        ticket_types = TicketBookingType.objects.filter(booking=booking)
        booking_ticket_types.append((booking, ticket_types))

    context = {
        'bookings': booking_ticket_types
    }

    return render(request, 'manage_client_bookings.html', context)

def validate_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
        # Update the booking status to 'confirmed'
    booking.status = 'confirmed'
    booking.save()
    return redirect('bookings:show_bookings', event_id=booking.event.event_id)  # Replace with your success URL
