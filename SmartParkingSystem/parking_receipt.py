"""Receipt generation for SmartParkingSystem"""
from datetime import datetime
from typing import Any


class ParkingReceipt:
    @staticmethod
    def generate_receipt(vehicle: Any, fee: float) -> str:
        """Generate a formatted parking receipt string.

        Parameters
        - vehicle: Vehicle instance (has vehicle_no, owner_name, entry_time, exit_time, slot_number)
        - fee: calculated parking fee
        """
        entry = vehicle.entry_time.strftime("%Y-%m-%d %H:%M:%S") if vehicle.entry_time else "N/A"
        exit_t = vehicle.exit_time.strftime("%Y-%m-%d %H:%M:%S") if vehicle.exit_time else "N/A"
        duration_seconds = (vehicle.exit_time - vehicle.entry_time).total_seconds() if (vehicle.exit_time and vehicle.entry_time) else 0
        duration_hours = round(duration_seconds / 3600, 2)

        lines = [
            "========== PARKING RECEIPT ==========",
            f"Vehicle No : {vehicle.vehicle_no}",
            f"Owner      : {vehicle.owner_name}",
            f"Vehicle Type: {vehicle.vehicle_type}",
            f"Slot No    : {vehicle.slot_number}",
            f"Entry Time : {entry}",
            f"Exit Time  : {exit_t}",
            f"Duration   : {duration_hours} hours",
            f"Amount Due : ${fee:.2f}",
            "======================================",
        ]
        return "\n".join(lines)
