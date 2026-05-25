Hospital Appointment Chatbot

This is a small Python project that lets a user book and manage hospital appointments through a text chat in the terminal. The chatbot can book, check, update, and cancel appointments, and can also answer a few basic hospital questions such as visiting hours.

The idea is to let someone type messages in plain English instead of using a form.



**What it can do**:

book a hospital appointment

store it with a 6-digit ID

check an appointment using the ID

update the date or time

cancel an appointment

remember your name during the chat

answer simple questions from a CSV (like “Where is radiology?”)



**How it works (short)** :

The chatbot looks at what you type, tries to match the intent using TF-IDF similarity, and then either:

starts booking using a step-by-step flow, or

shows hospital information from a small FAQ file.

Appointments are saved in a JSON file so they don’t disappear when the program closes.



**Files in the project** :

main.py – runs the chatbot

intents.py – example sentences for each intent

nlp_utils.py – text preprocessing + extracting names

booking.py – booking and updating logic

storage.py – saving and loading JSON data

state.py – keeps track of the booking progress

faq.py – reads the FAQ CSV and finds the closest answer

hospital_faq.csv – questions and answers

appointments.json – saved appointment data



**How to install**:

First install the requirements:

pip install -r requirements.txt

How to run


**In the terminal**:

python main.py


You will see a greeting and then you can start typing messages (for example, “book a hospital appointment”).

Type bye to exit.