import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_parking.settings')
import django
django.setup()
from django.template.loader import render_to_string
from parking_app.models import ParkingSlot, Vehicle

slots = ParkingSlot.objects.order_by('slot_number')
slots_info = []
for s in slots:
    p = Vehicle.objects.filter(slot=s, exit_time__isnull=True).first()
    slots_info.append({'slot': s, 'vehicle': p})

html = render_to_string('parking_app/index.html', {'slots_info': slots_info})
open('page.html', 'w', encoding='utf-8').write(html)
open('temp_index.html', 'w', encoding='utf-8').write(html)
print('WROTE page.html and temp_index.html; bytes=', len(html))
