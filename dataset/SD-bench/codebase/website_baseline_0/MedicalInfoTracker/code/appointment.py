class Appointment:
    def __init__(self, appointments: list):
        self.appointments = appointments

    def add_appointment(self, date: str, time: str, details: str):
        self.appointments.append(f"{date} {time}: {details}")

    def save(self, username: str):
        with open('appointments.txt', 'a') as file:
            file.write(f"{username}|{','.join(self.appointments)}\n")

    @staticmethod
    def load(username: str):
        appointments = Appointment([])
        try:
            with open('appointments.txt', 'r') as file:
                for line in file:
                    user, appointment_details = line.strip().split('|')
                    if user == username:
                        appointments.appointments = appointment_details.split(',')
                        break
        except FileNotFoundError:
            pass
        return appointments