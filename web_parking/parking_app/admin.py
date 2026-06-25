from django.contrib import admin, messages
from django.db import transaction
from django.utils import timezone
from .models import ParkingSlot, Vehicle, WaitingVehicle


def allocate_waiting_vehicle_to_slot(slot):
    next_wait = WaitingVehicle.objects.order_by('queued_at').first()
    if not next_wait:
        return None

    slot.occupied = True
    slot.save()
    Vehicle.objects.create(
        vehicle_no=next_wait.vehicle_no,
        owner_name=next_wait.owner_name,
        vehicle_type=next_wait.vehicle_type,
        slot=slot,
    )
    next_wait.delete()
    return slot.slot_number


@admin.register(ParkingSlot)
class ParkingSlotAdmin(admin.ModelAdmin):
    list_display = ('slot_number', 'occupied')


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_no', 'owner_name', 'vehicle_type', 'slot', 'entry_time', 'exit_time')
    
    def get_readonly_fields(self, request, obj=None):
        """Make slot and entry_time read-only since they're auto-set; vehicle_no is read-only only when editing."""
        if obj:  # editing existing
            return ('slot', 'entry_time', 'vehicle_no')
        return ('entry_time',)

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        # When an admin adds a new Vehicle via admin, force auto-allocation.
        if not change:  # new vehicle
            existing_active = Vehicle.objects.filter(vehicle_no=obj.vehicle_no, exit_time__isnull=True).exists()
            if existing_active:
                self.message_user(request, f"Vehicle {obj.vehicle_no} is already parked!", messages.ERROR)
                return

            slot = ParkingSlot.objects.filter(occupied=False).order_by('slot_number').first()
            if slot:
                slot.occupied = True
                slot.save()
                previous = Vehicle.objects.filter(vehicle_no=obj.vehicle_no, exit_time__isnull=False).order_by('-exit_time').first()
                if previous:
                    previous.owner_name = obj.owner_name
                    previous.vehicle_type = obj.vehicle_type
                    previous.entry_time = timezone.now()
                    previous.exit_time = None
                    previous.slot = slot
                    previous.save()
                    self.message_user(request, f"Re-parked {obj.vehicle_no} at slot {slot.slot_number}.", messages.SUCCESS)
                else:
                    obj.slot = slot
                    obj.exit_time = None
                    super().save_model(request, obj, form, change)
                    self.message_user(request, f"Parked {obj.vehicle_no} at slot {slot.slot_number}.", messages.SUCCESS)
            else:
                WaitingVehicle.objects.create(vehicle_no=obj.vehicle_no, owner_name=obj.owner_name, vehicle_type=obj.vehicle_type)
                self.message_user(request, f"Parking full. {obj.vehicle_no} added to waiting queue.", messages.INFO)
        else:
            super().save_model(request, obj, form, change)

    @transaction.atomic
    def delete_model(self, request, obj):
        freed_slot = None
        if obj.exit_time is None and obj.slot is not None:
            freed_slot = obj.slot
            freed_slot.occupied = False
            freed_slot.save()

        super().delete_model(request, obj)

        if freed_slot:
            allocated_slot = allocate_waiting_vehicle_to_slot(freed_slot)
            if allocated_slot:
                self.message_user(
                    request,
                    f"Vehicle from waiting queue has been automatically allocated to Slot {allocated_slot}.",
                    messages.SUCCESS,
                )

    @transaction.atomic
    def delete_queryset(self, request, queryset):
        freed_slots = []
        for obj in queryset.filter(exit_time__isnull=True, slot__isnull=False):
            slot = obj.slot
            if slot not in freed_slots:
                slot.occupied = False
                slot.save()
                freed_slots.append(slot)

        super().delete_queryset(request, queryset)

        for slot in freed_slots:
            allocated_slot = allocate_waiting_vehicle_to_slot(slot)
            if allocated_slot:
                self.message_user(
                    request,
                    f"Vehicle from waiting queue has been automatically allocated to Slot {allocated_slot}.",
                    messages.SUCCESS,
                )


@admin.register(WaitingVehicle)
class WaitingVehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_no', 'owner_name', 'vehicle_type', 'queued_at')
