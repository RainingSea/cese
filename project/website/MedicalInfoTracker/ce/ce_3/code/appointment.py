class Appointment:
    def __init__(self):
        self.appointments = self.load_appointments()

    def load_appointments(self):
        appointments = []
        with open('appointments.txt', 'r') as file:
            for line in file:
                appointments.append(line.strip().split('|'))
        return appointments

    def set_reminder(self, date: str, time: str, description: str) -> None:
        appointment = [date, time, description]
        self.appointments.append(appointment)
        with open('appointments.txt', 'a') as file:
            file.write('|'.join(appointment) + '\n')

    def get_reminders(self) -> list:
        return self.appointments