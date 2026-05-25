import storage

name_memory = None #stores user_name
booking_state = None #current booking_state(service,time,date,cnofirm)
booking_info = {} #stores temporary booking details
bookings = storage.load_appointments() #full list of saved appointments
update_mode = False #used to update appointment when it is True
update_index = None #Appointment updates based on index value stored here
