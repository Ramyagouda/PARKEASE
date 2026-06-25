from django.db import models
from django.utils import timezone
from django.conf import settings


class ParkingSlot(models.Model):
    slot_number = models.PositiveIntegerField(unique=True)
    occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Slot {self.slot_number} ({'Occupied' if self.occupied else 'Free'})"


class Vehicle(models.Model):
    vehicle_no = models.CharField(max_length=20, unique=True)
    owner_name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=20)
    entry_time = models.DateTimeField(default=timezone.now)
    exit_time = models.DateTimeField(null=True, blank=True)
    slot = models.ForeignKey(ParkingSlot, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.vehicle_no} - {self.owner_name}"


class WaitingVehicle(models.Model):
    vehicle_no = models.CharField(max_length=20)
    owner_name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=20)
    queued_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['queued_at']

    def __str__(self):
        return f"{self.vehicle_no} (queued at {self.queued_at})"
