import re
import random
import state
import storage


def generate_appointment_id():
    existing_ids = {str(a.get("id")) for a in state.bookings if "id" in a}
    while True:
        candidate = str(random.randint(100000, 999999))
        if candidate not in existing_ids:
            return candidate


def handle_booking_flow(text):
    
    t = (text or "").strip().lower()

    if t in ("cancel", "stop", "exit"):
        print("Chatbot: Okay, I've cancelled this process.")
        state.booking_state = None
        state.booking_info = {}
        state.update_mode = False
        state.update_index = None
        return True

    if state.booking_state == "ASK_SERVICE":
        if not text.strip():
            print("Chatbot: I didn't catch that. What kind of hospital appointment would you like to book?")
            print("Chatbot: For example: GP, cardiology, physiotherapy.")
            return True

        state.booking_info["service"] = text.strip()
        state.booking_state = "ASK_DATE"
        print(f"Chatbot: Great, a {state.booking_info['service']} hospital appointment.")
        print("Chatbot: On which date would you like the appointment?")
        print("Chatbot: Please use DD/MM/YYYY, for example 10/11/2025.")
        return True

    if state.booking_state == "ASK_DATE":
        if not re.match(r"^\d{1,2}/\d{1,2}/\d{4}$", text.strip()):
            print("Chatbot: I didn't understand that date.")
            print("Chatbot: Please use the format DD/MM/YYYY, for example 10/11/2025.")
            return True

        state.booking_info["date"] = text.strip()
        state.booking_state = "ASK_TIME"
        print("Chatbot: At what time would you like the appointment?")
        print("Chatbot: For example 14:30 or 2:30pm.")
        return True

    if state.booking_state == "ASK_TIME":
        if not text.strip():
            print("Chatbot: I didn't catch the time. Please say a time like 14:30 or 2:30pm.")
            return True

        state.booking_info["time"] = text.strip()
        state.booking_state = "CONFIRM"

        user_name = state.name_memory or "there"
        if state.update_mode:
            print(f"Chatbot: Okay {user_name}, you want to update your {state.booking_info['service']} hospital appointment")
        else:
            print(f"Chatbot: Okay {user_name}, you want a {state.booking_info['service']} hospital appointment")
        print(f"Chatbot: on {state.booking_info['date']} at {state.booking_info['time']}.")
        if state.update_mode:
            print("Chatbot: Should I update this appointment? (yes/no)")
        else:
            print("Chatbot: Should I confirm this booking? (yes/no)")
        return True

    if state.booking_state == "CONFIRM":
        if t in ("yes", "yeah", "y", "yep", "confirm"):
            if state.update_mode and state.update_index is not None and 0 <= state.update_index < len(state.bookings):
                appt = state.bookings[state.update_index]
                appt["service"] = state.booking_info.get("service", appt.get("service"))
                appt["date"] = state.booking_info.get("date", appt.get("date"))
                appt["time"] = state.booking_info.get("time", appt.get("time"))
                storage.save_appointments(state.bookings)
                print("Chatbot: Your hospital appointment has been updated!")
                if "id" in appt:
                    print(f"Chatbot: Appointment ID: {appt['id']}")
            else:
                new_id = generate_appointment_id()
                appointment = {
                    "id": new_id,
                    "name": state.name_memory,
                    **state.booking_info
                }
                state.bookings.append(appointment)
                storage.save_appointments(state.bookings)
                print("Chatbot: Your hospital appointment has been booked!")
                print(f"Chatbot: Your appointment ID is {new_id}. Please note it down.")
            print("Chatbot: You can later say 'Check my appointment 123456', 'Cancel my appointment 123456', or 'Update my appointment 123456'.")
            state.booking_state = None
            state.booking_info = {}
            state.update_mode = False
            state.update_index = None
            return True
        elif t in ("no", "n", "nope"):
            if state.update_mode:
                print("Chatbot: Okay, I won't update your appointment.")
            else:
                print("Chatbot: Okay, I won't book that appointment.")
            state.booking_state = None
            state.booking_info = {}
            state.update_mode = False
            state.update_index = None
            return True
        else:
            print("Chatbot: Please answer 'yes' or 'no' to confirm.")
            return True

    print("Chatbot: I'm in the middle of a hospital appointment process.")
    print("Chatbot: Please answer my question, or say 'cancel' to stop.")
    return True
