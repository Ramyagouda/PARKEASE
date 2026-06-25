🚗 **PARKEASE:Smart Parking Management System**
🎯 Problem Statement

Finding a parking space in crowded areas is time-consuming and inefficient. Traditional parking systems often rely on manual slot management, leading to poor space utilization, long waiting times, and difficulty in tracking parked vehicles.

The Smart Parking Management System automates parking operations by efficiently allocating parking slots, maintaining vehicle records, managing waiting vehicles, calculating parking fees, and generating receipts.

**📖 Project Overview**

The Smart Parking Management System is a console-based application developed using Python, Object-Oriented Programming (OOP), and Data Structures & Algorithms (DSA).

The system automatically assigns the nearest available parking slot to incoming vehicles, maintains vehicle information, manages waiting vehicles using a queue, calculates parking charges based on parking duration, and generates parking receipts.

**✨ Key Features**

🚘 Vehicle Management
Add vehicle entry
Remove vehicle exit
Duplicate vehicle validation
Vehicle information tracking
🅿️ Smart Slot Allocation
Automatic nearest-slot assignment
Efficient slot management using Min Heap
Real-time slot availability tracking
📋 Waiting Queue Management
FIFO-based waiting queue
Automatic slot assignment when a slot becomes available
💰 Parking Fee Calculation
Time-based parking charge calculation
Configurable hourly parking rate
🧾 Receipt Generation
Vehicle details
Entry and exit timestamps
Parking duration
Total fee
📊 Dashboard & Reports
Available slots count
Occupied slots count
Parked vehicle list
Waiting queue status
🛡️ Error Handling
Invalid vehicle number checks
Duplicate entry prevention
Safe vehicle removal

🛠️ Technology Stack


💻 Programming Language	Python 3.12+
🏗️ Development Paradigm	Object-Oriented Programming (OOP)
📚 Data Structures	Dictionary, Queue (Deque), Min Heap
📦 Libraries	datetime, heapq, collections.deque
🖥️ Interface	Console/CLI
🔄 Version Control	Git & GitHub
🌐 Platform	Windows/Linux/macOS
🧠 Data Structures Used
📖 Hash Map (Dictionary)
Stores parked vehicles
Enables O(1) average lookup time
📥 Queue (Deque)
Manages waiting vehicles
Follows FIFO principle
O(1) insertion and deletion
⚡ Priority Queue (Min Heap)
Stores available slot numbers
Allocates nearest available slot efficiently
O(log n) insertion and deletion

**🔄 Project Workflow**

1️⃣ Vehicle enters parking area
2️⃣ System checks slot availability
3️⃣ Nearest available slot is assigned
4️⃣ Vehicle details are stored
5️⃣ If no slot is available, vehicle joins waiting queue
6️⃣ Upon vehicle exit:
Parking fee is calculated
Receipt is generated
Slot becomes available
7️⃣ First vehicle from waiting queue gets the free slot automatically

🚀 Future Enhancements

📱 QR Code-based Parking
🌐 Web Dashboard
📡 IoT Sensor Integration
📲 Mobile Application

<img width="1727" height="911" alt="image" src="https://github.com/user-attachments/assets/21561e2d-9716-4ba3-9faf-ecceac9f1beb" />
fig. home page

<img width="1747" height="851" alt="image" src="https://github.com/user-attachments/assets/b583bb15-8511-4dc6-b935-2c02753d6e22" />
fig.parking slot with one empty slot and there is no waiting queue.

<img width="1452" height="511" alt="image" src="https://github.com/user-attachments/assets/e07b945f-cac8-476c-a907-ca8c0bbcc3ae" />
fig.parking vehicle

<img width="1196" height="507" alt="image" src="https://github.com/user-attachments/assets/d80ade2b-abd2-4815-9f1f-c3021becf264" />
fig.parking is full ,vehicle added to waiting queue

<img width="1677" height="772" alt="image" src="https://github.com/user-attachments/assets/34098994-9920-48a0-b6ef-3bb45be559d2" />
fig.waiting queue

<img width="1666" height="662" alt="image" src="https://github.com/user-attachments/assets/2549b702-257e-4312-a394-d2822e4b0716" />
fig.remove the vehicle

<img width="1677" height="857" alt="image" src="https://github.com/user-attachments/assets/757ecf5b-76da-4083-a963-c1ee6c639ce2" />
fig.dashboard

<img width="1877" height="912" alt="image" src="https://github.com/user-attachments/assets/b237fdfd-9133-40eb-bc49-bbed54502289" />
<img width="1881" height="491" alt="image" src="https://github.com/user-attachments/assets/1e72a7eb-9451-4398-aa8e-54039ba92344" />
<img width="1892" height="646" alt="image" src="https://github.com/user-attachments/assets/84303039-9c80-453b-8f0d-ce3671abf49d" />
<img width="1677" height="295" alt="image" src="https://github.com/user-attachments/assets/336223df-af87-4a90-844d-07dda92787b9" />
admin panel for managing slots,vehicles and waiting queues







