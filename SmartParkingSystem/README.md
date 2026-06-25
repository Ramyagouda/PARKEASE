# Smart Parking Management System (Console)

Complete, modular, industry-ready Smart Parking Management System implemented in Python (OOP + DSA).

**Project Structure**

SmartParkingSystem/
│
├── vehicle.py
├── parking_slot.py
├── parking_receipt.py
├── parking_manager.py
├── utils.py
├── main.py
├── README.md
└── requirements.txt

**Run (recommended)**

From the folder that contains the `SmartParkingSystem` package run:

```bash
python -m SmartParkingSystem.main
```

This runs the console CLI.

**Installation**

- Python 3.12+ is required.
- No external packages required.
- Create a virtualenv (optional):

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r SmartParkingSystem/requirements.txt
```

**Features**

- Vehicle Entry with validation
- Automatic nearest-slot allocation (min-heap)
- O(1) vehicle lookup (dictionary)
- Waiting queue using FIFO (`collections.deque`)
- Parking fee calculation (configurable hourly rate)
- Receipt generation
- Dashboard and report generation
- Error handling for duplicates and invalid input

**DSA Explanation (in-code)**

- HashMap (dictionary): provides O(1) average time lookup for vehicles by registration number.
- Queue (deque): provides O(1) enqueue/dequeue for waiting vehicles (FIFO behavior).
- Priority Queue (heapq): provides O(log n) allocation for the nearest available slot, ensuring efficient allocation.

Time complexities are included in `parking_manager.py` comments.

**Sample Execution Output (excerpt)**

1) Park a vehicle

> Parked vehicle MH12-AB1234 at slot 1.

2) Remove a vehicle and print receipt

> ========== PARKING RECEIPT ==========
> Vehicle No : MH12-AB1234
> Owner      : Alice
> Vehicle Type: Car
> Slot No    : 1
> Entry Time : 2026-06-23 10:00:00
> Exit Time  : 2026-06-23 12:30:00
> Duration   : 3.0 hours
> Amount Due : $60.00
> ======================================

**Architecture Diagram (text)**

ParkingManager
  - maintains -> List[ParkingSlot] (all slots)
  - maintains -> Heap (available slot numbers)
  - maintains -> Dict vehicle_no -> Vehicle (parked vehicles)
  - maintains -> Deque (waiting vehicles)

Vehicle <--- stored in ---- ParkingManager/vehicle_map

When slot freed -> pop from waiting queue (if present) -> assign slot

**Resume-ready project description**

Developed a modular Smart Parking Management System in Python using object-oriented design and core data structures (hash map, queue, priority queue). Implemented efficient slot allocation, O(1) vehicle lookup, FIFO waiting queue, configurable fee calculation, and receipt generation. System is console-based and readily extensible for integration with web/mobile frontends and IoT sensors.

**Future Enhancements**

- QR Code Parking (check-in/out using QR)
- IoT Parking Sensors (automatic occupancy updates)
- Real-Time Dashboard (websocket-powered dashboard)
- Mobile App Integration (booking + navigation)
- AI-Based Slot Prediction (time-series demand forecasting)

**Files to inspect/start**

- [SmartParkingSystem/main.py](SmartParkingSystem/main.py)
- [SmartParkingSystem/parking_manager.py](SmartParkingSystem/parking_manager.py)
