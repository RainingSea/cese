class AppointmentManager:
    def __init__(self, appointments_file: str):
        self.appointments_file = appointments_file
        self.load_appointments()

    def load_appointments(self):
        self.appointments = {}

        with open(self.appointments_file, 'r') as file:
            for line in file:
                user_id, appointment = line.strip().split('|')
                if user_id not in self.appointments:
                    self.appointments[user_id] = []
                self.appointments[user_id].append(appointment)

    def set_appointment(self, user_id: str, appointment: str):
        with open(self.appointments_file, 'a') as file:
            file.write(f"{user_id}|{appointment}\n")
        if user_id not in self.appointments:
            self.appointments[user_id] = []
        self.appointments[user_id].append(appointment)

    def get_appointments(self, user_id: str):
        return self.appointments.get(user_id, [])