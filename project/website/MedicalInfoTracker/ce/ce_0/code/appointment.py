class Appointment:
    def __init__(self):
        self.appointments = []

    def add_appointment(self, date: str, time: str, description: str) -> None:
        self.appointments.append({'date': date, 'time': time, 'description': description})

    def save(self) -> None:
        with open('appointments.txt', 'w') as f:
            for appointment in self.appointments:
                f.write(f"{appointment['date']}|{appointment['time']}|{appointment['description']}\n")

    @staticmethod
    def load() -> 'Appointment':
        appointment = Appointment()
        try:
            with open('appointments.txt', 'r') as f:
                for line in f:
                    date, time, description = line.strip().split('|')
                    appointment.add_appointment(date, time, description)
        except FileNotFoundError:
            pass
        return appointment