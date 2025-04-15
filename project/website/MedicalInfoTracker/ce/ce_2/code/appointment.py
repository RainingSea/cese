class Appointment:
    def __init__(self):
        self.appointments = []

    def add_appointment(self, date: str, time: str, description: str) -> None:
        self.appointments.append({"date": date, "time": time, "description": description})

    def view_appointments(self) -> list:
        return self.appointments

    def remove_appointment(self, index: int) -> None:
        if 0 <= index < len(self.appointments):
            del self.appointments[index]