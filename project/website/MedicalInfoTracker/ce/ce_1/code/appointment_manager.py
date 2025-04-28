class AppointmentManager:
    def __init__(self):
        self.appointments = self.load_appointments()

    def load_appointments(self):
        appointments = []
        try:
            with open('appointments.txt', 'r') as file:
                for line in file:
                    appointments.append(line.strip())
        except FileNotFoundError:
            pass
        return appointments

    def set_reminder(self, date: str, time: str):
        self.appointments.append(f"Reminder: {date} at {time}")
        self.save_appointments()

    def view_reminders(self):
        return self.appointments

    def save_appointments(self):
        with open('appointments.txt', 'w') as file:
            for appointment in self.appointments:
                file.write(f"{appointment}\n")