"""Vehicle model for SmartParkingSystem

Contains the Vehicle dataclass which stores vehicle details and timestamps.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Vehicle:
    vehicle_no: str
    owner_name: str
    vehicle_type: str
    entry_time: Optional[datetime] = field(default=None)
    exit_time: Optional[datetime] = field(default=None)
    slot_number: Optional[int] = field(default=None)

    def mark_entry(self) -> None:
        """Record entry time for vehicle."""
        self.entry_time = datetime.now()

    def mark_exit(self) -> None:
        """Record exit time for vehicle."""
        self.exit_time = datetime.now()
