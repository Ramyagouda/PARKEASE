"""Console-based CLI for SmartParkingSystem

Run as module from parent folder:

    python -m SmartParkingSystem.main

"""
from typing import Optional

from .parking_manager import ParkingManager


def main():
    manager = ParkingManager(total_slots=10, hourly_rate=20.0)

    menu = """
Smart Parking Management System
1. Park Vehicle
2. Remove Vehicle
3. Search Vehicle
4. Display Available Slots
5. Display Occupied Slots
6. Show Waiting Queue
7. Parking Statistics
8. Generate Report
9. Exit
"""

    while True:
        print(menu)
        try:
            choice = int(input("Enter choice: ").strip())
        except (ValueError, KeyboardInterrupt):
            print("Invalid input. Please enter a number between 1-9.")
            continue

        if choice == 1:
            vehicle_no = input("Vehicle Number: ").strip()
            owner_name = input("Owner Name: ").strip()
            vehicle_type = input("Vehicle Type (Car/Bike/Truck): ").strip()
            msg = manager.add_vehicle(vehicle_no, owner_name, vehicle_type)
            print(msg)

        elif choice == 2:
            vehicle_no = input("Vehicle Number to remove: ").strip()
            receipt = manager.remove_vehicle(vehicle_no)
            if receipt is None:
                print("Error removing vehicle.")
            else:
                print(receipt)

        elif choice == 3:
            vehicle_no = input("Vehicle Number to search: ").strip()
            print(manager.search_vehicle(vehicle_no))

        elif choice == 4:
            slots = manager.display_available_slots()
            print(f"Available Slots ({len(slots)}): {slots}")

        elif choice == 5:
            occupied = manager.display_occupied_slots()
            if not occupied:
                print("No occupied slots.")
            else:
                for line in occupied:
                    print(line)

        elif choice == 6:
            q = manager.show_waiting_queue()
            if not q:
                print("Waiting queue is empty.")
            else:
                for line in q:
                    print(line)

        elif choice == 7:
            stats = manager.generate_statistics()
            print("Parking Statistics:")
            for k, v in stats.items():
                print(f"- {k}: {v}")

        elif choice == 8:
            print(manager.generate_report())

        elif choice == 9:
            print("Exiting. Goodbye!")
            break

        else:
            print("Invalid choice. Please select from 1-9.")


if __name__ == "__main__":
    main()
