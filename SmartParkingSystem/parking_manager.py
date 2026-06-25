"""
ParkingManager: core logic for SmartParkingSystem

DSA Notes:
- HashMap (dictionary) `vehicle_map` is used for O(1) vehicle lookup by registration number.
- Queue (`collections.deque`) is used for waiting vehicles (FIFO) with O(1) enqueue/dequeue.
- Priority Queue (`heapq`) is used for allocating nearest available slot. Popping/pushing is O(log n).

Time complexities (major operations):
- search_vehicle: O(1)
- add_vehicle (allocate slot): O(log n) due to heap pop (slot allocation)
- remove_vehicle: O(log n) for pushing freed slot back to heap + O(1) dictionary ops
- waiting queue enqueue/dequeue: O(1)

"""
from collections import deque
import heapq
from datetime import datetime
from math import ceil
from typing import Dict, List, Optional

from .vehicle import Vehicle
from .parking_slot import ParkingSlot
from .parking_receipt import ParkingReceipt
from .utils import validate_vehicle_no, normalize_vehicle_no


class ParkingManager:
    def __init__(self, total_slots: int = 10, hourly_rate: float = 10.0):
        self.total_slots = total_slots
        self.hourly_rate = hourly_rate

        # List: store all parking slots (index = slot_number - 1)
        self.slots: List[ParkingSlot] = [ParkingSlot(i + 1) for i in range(total_slots)]

        # Priority queue (min-heap) of available slot numbers => nearest slot has smallest number
        self.available_slots: List[int] = [i + 1 for i in range(total_slots)]
        heapq.heapify(self.available_slots)

        # HashMap: vehicle_no -> Vehicle (fast O(1) lookup)
        self.vehicle_map: Dict[str, Vehicle] = {}

        # Waiting queue (FIFO) for vehicles when parking is full
        self.waiting_queue: deque[Vehicle] = deque()

    def add_vehicle(self, vehicle_no: str, owner_name: str, vehicle_type: str) -> str:
        """Register and park a vehicle. If full, add to waiting queue.

        Returns a status message.
        """
        if not validate_vehicle_no(vehicle_no):
            return "Invalid vehicle number format." 

        vehicle_no = normalize_vehicle_no(vehicle_no)

        # Prevent duplicate vehicle across parked vehicles
        if vehicle_no in self.vehicle_map:
            return f"Vehicle {vehicle_no} is already parked in slot {self.vehicle_map[vehicle_no].slot_number}."

        # Prevent duplicate in waiting queue
        for v in self.waiting_queue:
            if v.vehicle_no == vehicle_no:
                return f"Vehicle {vehicle_no} is already in waiting queue at position {list(self.waiting_queue).index(v)+1}."

        vehicle = Vehicle(vehicle_no=vehicle_no, owner_name=owner_name, vehicle_type=vehicle_type)

        if self.available_slots:
            slot_no = heapq.heappop(self.available_slots)  # O(log n)
            self._assign_slot(vehicle, slot_no)
            self.vehicle_map[vehicle_no] = vehicle  # O(1)
            return f"Parked vehicle {vehicle_no} at slot {slot_no}."
        else:
            self.waiting_queue.append(vehicle)  # O(1)
            return f"Parking full. Vehicle {vehicle_no} added to waiting queue position {len(self.waiting_queue)}."

    def _assign_slot(self, vehicle: Vehicle, slot_no: int) -> None:
        """Internal: mark slot occupied and set vehicle entry."""
        slot = self.slots[slot_no - 1]
        slot.occupied = True
        slot.vehicle_no = vehicle.vehicle_no
        vehicle.slot_number = slot_no
        vehicle.mark_entry()

    def remove_vehicle(self, vehicle_no: str) -> Optional[str]:
        """Remove vehicle from parking, calculate fee, generate receipt.

        If waiting queue has vehicles, allocate freed slot to next in queue.
        Returns receipt text or error message.
        """
        vehicle_no = normalize_vehicle_no(vehicle_no)
        if vehicle_no not in self.vehicle_map:
            return f"Vehicle {vehicle_no} not found in parking." 

        vehicle = self.vehicle_map.pop(vehicle_no)
        vehicle.mark_exit()

        # Free the slot
        slot_no = vehicle.slot_number
        if slot_no is not None:
            slot = self.slots[slot_no - 1]
            slot.occupied = False
            slot.vehicle_no = None
            heapq.heappush(self.available_slots, slot_no)  # O(log n)

        fee = self.calculate_fee(vehicle)
        receipt = ParkingReceipt.generate_receipt(vehicle, fee)

        # If waiting queue not empty, allocate slot to next vehicle
        if self.waiting_queue and self.available_slots:
            next_vehicle = self.waiting_queue.popleft()  # O(1)
            next_slot = heapq.heappop(self.available_slots)  # O(log n)
            self._assign_slot(next_vehicle, next_slot)
            self.vehicle_map[next_vehicle.vehicle_no] = next_vehicle

        return receipt

    def search_vehicle(self, vehicle_no: str) -> str:
        """Search for vehicle by registration number (O(1))."""
        vehicle_no = normalize_vehicle_no(vehicle_no)
        if vehicle_no in self.vehicle_map:
            v = self.vehicle_map[vehicle_no]
            return f"Found parked vehicle {v.vehicle_no} at slot {v.slot_number}. Entry: {v.entry_time}."

        # Check waiting queue (O(n))
        for idx, v in enumerate(self.waiting_queue, start=1):
            if v.vehicle_no == vehicle_no:
                return f"Vehicle {vehicle_no} is in waiting queue at position {idx}."

        return f"Vehicle {vehicle_no} not found."

    def display_available_slots(self) -> List[int]:
        """Return sorted list of available slots."""
        # Make a sorted copy to avoid mutating heap
        return sorted(self.available_slots)

    def display_occupied_slots(self) -> List[str]:
        """Return list of occupied slot summaries."""
        result = []
        for slot in self.slots:
            if slot.occupied and slot.vehicle_no:
                v = self.vehicle_map.get(slot.vehicle_no)
                result.append(f"Slot {slot.slot_number}: {slot.vehicle_no} (Owner: {v.owner_name})")
        return result

    def show_waiting_queue(self) -> List[str]:
        return [f"{idx+1}. {v.vehicle_no} ({v.owner_name})" for idx, v in enumerate(self.waiting_queue)]

    def calculate_fee(self, vehicle: Vehicle) -> float:
        """Calculate parking fee based on rounded-up hours.

        Charging policy: every partial hour counts as a full hour (ceil).
        """
        if not vehicle.entry_time or not vehicle.exit_time:
            return 0.0
        seconds = (vehicle.exit_time - vehicle.entry_time).total_seconds()
        hours = ceil(seconds / 3600)
        return float(hours * self.hourly_rate)

    def generate_statistics(self) -> Dict[str, int]:
        available = len(self.available_slots)
        occupied = len(self.vehicle_map)
        waiting = len(self.waiting_queue)
        return {
            "total_slots": self.total_slots,
            "available_slots": available,
            "occupied_slots": occupied,
            "waiting_vehicles": waiting,
        }

    def generate_report(self) -> str:
        """Return a multi-line report of current parked vehicles and stats."""
        lines = ["--- Parking Report ---"]
        stats = self.generate_statistics()
        lines.append(f"Total Slots: {stats['total_slots']}")
        lines.append(f"Available Slots: {stats['available_slots']}")
        lines.append(f"Occupied Slots: {stats['occupied_slots']}")
        lines.append(f"Waiting Vehicles: {stats['waiting_vehicles']}")
        lines.append("")
        lines.append("Parked Vehicles:")
        for v in self.vehicle_map.values():
            lines.append(f"- {v.vehicle_no} | Owner: {v.owner_name} | Slot: {v.slot_number} | Entry: {v.entry_time}")

        if self.waiting_queue:
            lines.append("")
            lines.append("Waiting Queue:")
            for idx, v in enumerate(self.waiting_queue, start=1):
                lines.append(f"{idx}. {v.vehicle_no} | Owner: {v.owner_name}")

        return "\n".join(lines)
