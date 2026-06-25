from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from .models import ParkingSlot, Vehicle, WaitingVehicle
from django import forms
from math import ceil


class ParkForm(forms.Form):
    vehicle_no = forms.CharField(max_length=20)
    owner_name = forms.CharField(max_length=100)
    vehicle_type = forms.CharField(max_length=20)


class RemoveForm(forms.Form):
    vehicle_no = forms.CharField(max_length=20)


def ensure_slots():
    total = settings.TOTAL_SLOTS
    existing = ParkingSlot.objects.count()
    if existing < total:
        for i in range(existing + 1, total + 1):
            ParkingSlot.objects.create(slot_number=i)


def landing(request):
    """Landing/splash page with motivational quote."""
    return render(request, 'parking_app/landing.html')


def home(request):
    """Home page showing parking slots and waiting queue."""
    ensure_slots()
    slots = ParkingSlot.objects.order_by('slot_number')
    # build slot entries by querying the parked vehicle for each slot
    slots_info = []
    for slot in slots:
        parked = Vehicle.objects.filter(slot=slot, exit_time__isnull=True).first()
        slots_info.append({'slot': slot, 'vehicle': parked})

    # also include the waiting queue (ordered by queued_at)
    waiting_list = WaitingVehicle.objects.order_by('queued_at')

    return render(request, 'parking_app/index.html', {
        'slots_info': slots_info,
        'waiting_list': waiting_list,
    })


def search(request):
    q = request.GET.get('q', '').upper().strip()
    results = []
    if q:
        results = list(Vehicle.objects.filter(vehicle_no__icontains=q))
    return render(request, 'parking_app/search_results.html', {'query': q, 'results': results})


@transaction.atomic
def park_vehicle(request):
    ensure_slots()
    msg = None
    if request.method == 'POST':
        form = ParkForm(request.POST)
        if form.is_valid():
            vehicle_no = form.cleaned_data['vehicle_no'].upper().strip()
            owner_name = form.cleaned_data['owner_name']
            vehicle_type = form.cleaned_data['vehicle_type']

            # check duplicate active parking
            if Vehicle.objects.filter(vehicle_no=vehicle_no, exit_time__isnull=True).exists():
                msg = f"Vehicle {vehicle_no} is already parked."
            else:
                slot = ParkingSlot.objects.filter(occupied=False).order_by('slot_number').first()
                if slot:
                    slot.occupied = True
                    slot.save()
                    previous = Vehicle.objects.filter(vehicle_no=vehicle_no, exit_time__isnull=False).order_by('-exit_time').first()
                    if previous:
                        previous.owner_name = owner_name
                        previous.vehicle_type = vehicle_type
                        previous.entry_time = timezone.now()
                        previous.exit_time = None
                        previous.slot = slot
                        previous.save()
                        msg = f"Re-parked {vehicle_no} at slot {slot.slot_number}."
                    else:
                        Vehicle.objects.create(vehicle_no=vehicle_no, owner_name=owner_name, vehicle_type=vehicle_type, slot=slot)
                        msg = f"Parked {vehicle_no} at slot {slot.slot_number}."
                else:
                    WaitingVehicle.objects.create(vehicle_no=vehicle_no, owner_name=owner_name, vehicle_type=vehicle_type)
                    msg = f"Parking full. {vehicle_no} added to waiting queue."
    else:
        form = ParkForm()
    return render(request, 'parking_app/park.html', {'form': form, 'msg': msg})


@transaction.atomic
def remove_vehicle(request):
    msg = None
    receipt = None
    if request.method == 'POST':
        form = RemoveForm(request.POST)
        if form.is_valid():
            vehicle_no = form.cleaned_data['vehicle_no'].upper().strip()
            try:
                v = Vehicle.objects.get(vehicle_no=vehicle_no, exit_time__isnull=True)
            except Vehicle.DoesNotExist:
                msg = f"Vehicle {vehicle_no} not found in parking."
            else:
                v.exit_time = timezone.now()
                # calculate fee
                seconds = (v.exit_time - v.entry_time).total_seconds()
                hours = ceil(seconds / 3600) if seconds > 0 else 1
                fee = hours * settings.HOURLY_RATE
                slot = v.slot
                v.slot = None
                v.save()
                if slot:
                    slot.occupied = False
                    slot.save()

                # allocate to waiting
                next_wait = WaitingVehicle.objects.order_by('queued_at').first()
                if next_wait and slot:
                    slot.occupied = True
                    slot.save()
                    # reuse any existing Vehicle record with this vehicle_no to avoid UNIQUE constraint failures
                    prev = Vehicle.objects.filter(vehicle_no=next_wait.vehicle_no).order_by('-entry_time').first()
                    if prev:
                        prev.owner_name = next_wait.owner_name
                        prev.vehicle_type = next_wait.vehicle_type
                        prev.entry_time = timezone.now()
                        prev.exit_time = None
                        prev.slot = slot
                        prev.save()
                    else:
                        Vehicle.objects.create(vehicle_no=next_wait.vehicle_no, owner_name=next_wait.owner_name, vehicle_type=next_wait.vehicle_type, slot=slot)
                    next_wait.delete()

                receipt = {
                    'vehicle_no': vehicle_no,
                    'owner': v.owner_name,
                    'vehicle_type': v.vehicle_type,
                    'slot': slot.slot_number if slot else 'N/A',
                    'entry': v.entry_time,
                    'exit': v.exit_time,
                    'fee': fee,
                }
    else:
        form = RemoveForm()
    return render(request, 'parking_app/remove.html', {'form': form, 'msg': msg, 'receipt': receipt})


def dashboard(request):
    ensure_slots()
    total = ParkingSlot.objects.count()
    available = ParkingSlot.objects.filter(occupied=False).count()
    occupied = ParkingSlot.objects.filter(occupied=True).count()
    waiting = WaitingVehicle.objects.count()
    vehicles = Vehicle.objects.filter(exit_time__isnull=True)
    waiting_list = WaitingVehicle.objects.all()
    # today's bookings and chart data (last 7 days)
    from django.utils import timezone
    from datetime import timedelta
    today = timezone.localdate()
    # bookings that started today
    todays_bookings_qs = Vehicle.objects.filter(entry_time__date=today)
    todays_bookings = list(todays_bookings_qs.order_by('-entry_time')[:50])

    # last 7 days bookings counts
    days = []
    bookings_series = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        days.append(day.strftime('%b %d'))
        cnt = Vehicle.objects.filter(entry_time__date=day).count()
        bookings_series.append(cnt)

    return render(request, 'parking_app/dashboard.html', {
        'total': total,
        'available': available,
        'occupied': occupied,
        'waiting': waiting,
        'vehicles': vehicles,
        'waiting_list': waiting_list,
        'hourly_rate': settings.HOURLY_RATE,
        'todays_bookings': todays_bookings,
        'days_labels': days,
        'bookings_series': bookings_series,
    })
