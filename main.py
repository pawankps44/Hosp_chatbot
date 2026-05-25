from nlp_utils import extract_name
from intents import detect_intent_cosine
from booking import handle_booking_flow
import state
import storage
import re
import faq


def greet():
    
    print("\n\n\nChatbot: Hello! I’m your hospital appointment assistant.")
    print("Chatbot: I can help you book, cancel, check, and update your hospital appointments.")
    print("Chatbot: I can also answer some common hospital questions, like visiting hours or department locations.")
    print("Chatbot: When I book an appointment, I will give you a 6-digit appointment ID.")
    print("Chatbot: You can use that ID to check, cancel, or update your appointment, for example: 'Check my appointment 123456'.")
    print("Chatbot: How are you?\n")
    print("Type 'bye' at any time to exit.\n")


def get_user_input():
    return input("You: ").strip()


def extract_id_from_text(text):
    m = re.search(r"\b(\d{6})\b", text)
    if m:
        return m.group(1)
    return None


def find_appointment_by_id(appt_id):
    for i, appt in enumerate(state.bookings): #looping through booking using id and boookings one by one
        if str(appt.get("id")) == str(appt_id):
            return i, appt
    return None, None


def handle_message(text):
    
    if state.booking_state is not None:
        handle_booking_flow(text)
        return

    intent = detect_intent_cosine(text)


    if intent == "empty":
        print("Chatbot: I didn't catch that — can you type that again?")
        return

    if intent == "goodbye":
        print("Chatbot: Goodbye! Take care.")
        return

    if intent == "greet_respond":
        print("Chatbot: That's good to hear. What is your name?")
        return

    if intent == "provide_name":
        name_candidate = extract_name(text)
        if name_candidate:
            state.name_memory = name_candidate
            print(f"Chatbot: Nice to meet you, {state.name_memory}!")
            print("Chatbot: I can help you with hospital appointments.")
        else:
            print("Chatbot: I didn't catch your name. Please say 'My name is ...' or 'Call me ...'")
        return

    if intent == "ask_name":
        if state.name_memory:
            print(f"Chatbot: Your name is {state.name_memory}.")
        else:
            print("Chatbot: I don't know your name yet — please say 'My name is ...' so I can remember it.")
        return

    if intent == "greeting":
        if state.name_memory:
            print(f"Chatbot: Hi {state.name_memory}! How can I help with your hospital appointments?")
        else:
            print("Chatbot: Hi! I'm your hospital appointment assistant.")
            print("Chatbot: What's your name? (please say 'My name is ...')")
        return

    if intent == "how_are_you":
        print("Chatbot: I'm doing well, thanks!")
        print("Chatbot: I can help you book, cancel, check, or update a hospital appointment, and answer some hospital information questions.")
        return

    if intent == "ask_capabilities":
        print("Chatbot: I can help with booking new hospital appointments,")
        print("Chatbot: cancelling existing ones, checking your appointment details, updating an existing appointment,")
        print("Chatbot: and answering some common hospital questions like visiting hours and department locations.")
        return

    if intent == "hospital_info":
        answer = faq.answer_faq(text)
        if answer:
            print(f"Chatbot: {answer}")
        else:
            print("Chatbot: I am not sure about that hospital information.")
            print("Chatbot: Please try asking in a different way or check with the hospital staff.")
        return

    if intent == "book_appointment":

        t = (text or "").lower()

        if "check" in t or "show" in t or "details" in t: #view existing appointment
            if not state.bookings:
                print("Chatbot: You don't have any hospital appointments booked yet.")
                return
            appt_id = extract_id_from_text(text) #checking user text for six digit number using regex
            if not appt_id:
                print("Chatbot: Please include your 6-digit appointment ID, for example: 'Check my appointment 123456'.")
                return
            idx, appt = find_appointment_by_id(appt_id)  #returns index and whole appointment details
            if appt is None:
                print(f"Chatbot: I couldn't find any appointment with ID {appt_id}.")
                return
            name = appt.get("name") or "you"
            print(f"Chatbot: I have a {appt['service']} hospital appointment for {name}")
            print(f"Chatbot: on {appt['date']} at {appt['time']}.")
            print(f"Chatbot: Appointment ID: {appt['id']}")
            return

        if "cancel" in t: #cancel existing appointment
            if not state.bookings:
                print("Chatbot: There is no hospital appointment to cancel.")
                return
            appt_id = extract_id_from_text(text)
            if not appt_id:
                print("Chatbot: Please include your 6-digit appointment ID, for example: 'Cancel my appointment 123456'.")
                return
            idx, appt = find_appointment_by_id(appt_id)
            if appt is None:
                print(f"Chatbot: I couldn't find any appointment with ID {appt_id}.")
                return
            removed = state.bookings.pop(idx) #removing using index
            storage.save_appointments(state.bookings) #saving after popping
            print(f"Chatbot: I have cancelled your {removed['service']} hospital appointment")
            print(f"Chatbot: which was on {removed['date']} at {removed['time']}.")
            print(f"Chatbot: Appointment ID was: {removed['id']}")
            return

        if "update" in t or "reschedule" in t or "change" in t: #update existing appointment
            if not state.bookings:
                print("Chatbot: You don't have any hospital appointments to update.")
                return
            appt_id = extract_id_from_text(text)
            if not appt_id:
                print("Chatbot: Please include your 6-digit appointment ID, for example: 'Update my appointment 123456'.")
                return
            idx, appt = find_appointment_by_id(appt_id)
            if appt is None:
                print(f"Chatbot: I couldn't find any appointment with ID {appt_id}.")
                return
            name = appt.get("name") or "you"
            print(f"Chatbot: You currently have a {appt['service']} hospital appointment for {name}")
            print(f"Chatbot: on {appt['date']} at {appt['time']}.")
            print(f"Chatbot: Appointment ID: {appt['id']}")
            state.update_mode = True
            state.update_index = idx
            state.booking_info = {
                "service": appt["service"]
            }
            state.booking_state = "ASK_DATE"
            print("Chatbot: Let's update this appointment.")
            print("Chatbot: On which new date would you like the appointment?")
            print("Chatbot: Please use DD/MM/YYYY, for example 10/11/2025.")
            return
        
        #comes here for new appointment booking

        if not state.name_memory:
            print("Chatbot: Before we continue, may I know your name?")
            print("Chatbot: Please say 'My name is ...'")
        else:
            state.update_mode = False 
            state.update_index = None
            state.booking_state = "ASK_SERVICE" #sets booking state to this, so that booking_state is not None to trigger handle_booking_flow
            state.booking_info = {}
            print(f"Chatbot: Okay {state.name_memory}, let's book a hospital appointment.")
            print("Chatbot: What type of hospital appointment would you like to book?")
            print("Chatbot: For example: GP, cardiology, physiotherapy.")
        return

    print("Chatbot: I didn’t quite understand that.")
    print("Chatbot: Try saying things like:")
    print("  - 'Book a hospital appointment'")
    print("  - 'Cancel my appointment 123456'")
    print("  - 'Check my appointment 123456'")
    print("  - 'Update my appointment 123456'")
    print("  - 'What are visiting hours?'")
    print("  - 'Where is the radiology department?'")
    print("  - 'What's my name?'")
    print("  - 'How are you?' or 'What can you do?'")


def main():
    greet()
    while True:
        user_text = get_user_input()
        if user_text.strip().lower() == "bye":
            print("Chatbot: Goodbye! Take care.")
            break
        handle_message(user_text)


if __name__ == "__main__":
    main()
