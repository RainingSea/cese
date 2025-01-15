class Appointment:
    def __init__(self, username: str):
        self.username = username
        self.reminders = []

    def add_reminder(self, reminder: str):
        self.reminders.append(reminder)

    def save(self):
        with open('appointments.txt', 'a') as file:
            file.write(f"{self.username}|{','.join(self.reminders)}\n")

    @staticmethod
    def load(username: str):
        with open('appointments.txt', 'r') as file:
            for line in file:
                appointment_data = line.strip().split('|')
                if appointment_data[0] == username:
                    appointment = Appointment(appointment_data[0])
                    appointment.reminders = appointment_data[1].split(',') if appointment_data[1] else []
                    return appointment
        return None