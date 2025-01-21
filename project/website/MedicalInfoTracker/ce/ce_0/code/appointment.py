class Appointment:
    def __init__(self):
        self.appointments = []

    def set_appointment(self, date: str, time: str, description: str) -> None:
        self.appointments.append({'date': date, 'time': time, 'description': description})

    def get_appointments(self) -> list:
        return self.appointments