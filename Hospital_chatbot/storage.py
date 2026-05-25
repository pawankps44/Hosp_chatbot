import json
import os

APPOINTMENTS_FILE = "appointments.json"


def load_appointments():
    if not os.path.exists(APPOINTMENTS_FILE):
        return []
    try:
        with open(APPOINTMENTS_FILE, "r") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data #loads data into bookings state in state.py when called
        return []
    except Exception:
        return []


def save_appointments(appointments):
    with open(APPOINTMENTS_FILE, "w") as f:
        json.dump(appointments, f, indent=2) #writing new patient data in Appointments.json
