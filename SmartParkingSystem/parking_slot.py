"""ParkingSlot model for SmartParkingSystem

Simple dataclass representing a parking slot.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ParkingSlot:
    slot_number: int
    occupied: bool = False
    vehicle_no: Optional[str] = None
