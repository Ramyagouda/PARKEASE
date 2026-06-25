"""Automated smoke test for SmartParkingSystem.

Simulates parking operations, waiting queue behavior, slot allocation,
fee calculation, and receipt generation.
"""
from datetime import timedelta

from .parking_manager import ParkingManager


def run_smoke_test():
    mgr = ParkingManager(total_slots=3, hourly_rate=20.0)

    print(mgr.add_vehicle("MH12-AB1234", "Alice", "Car"))
    print(mgr.add_vehicle("KA01-XY9999", "Bob", "Bike"))
    print(mgr.add_vehicle("DL4C-AB123", "Charlie", "Truck"))

    # This one should go to waiting queue
    print(mgr.add_vehicle("TN09-ZZ111", "Daisy", "Car"))

    print("Available slots:", mgr.display_available_slots())
    print("Occupied slots:", mgr.display_occupied_slots())
    print("Waiting queue:", mgr.show_waiting_queue())

    # Simulate passage of time for the first parked vehicle
    v_no = "MH12-AB1234"
    v = mgr.vehicle_map.get(v_no)
    if v:
        v.entry_time -= timedelta(hours=2, minutes=30)

    # Remove vehicle and print receipt
    receipt = mgr.remove_vehicle(v_no)
    print("Receipt for", v_no)
    print(receipt)

    print("After removal - Occupied slots:", mgr.display_occupied_slots())
    print("After removal - Waiting queue:", mgr.show_waiting_queue())
    print("Statistics:", mgr.generate_statistics())
    print("Full Report:\n", mgr.generate_report())


if __name__ == "__main__":
    run_smoke_test()
