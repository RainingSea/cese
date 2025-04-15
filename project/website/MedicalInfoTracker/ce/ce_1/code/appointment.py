class Appointment:
    def __init__(self):
        self.appointments = []

    def add_appointment(self, date: str, time: str, description: str) -> None:
        self.appointments.append({'date': date, 'time': time, 'description': description})
        self.save()

    def save(self) -> None:
        with open('appointments.txt', 'w') as f:
            for appointment in self.appointments:
                f.write(f"{appointment['date']}|{appointment['time']}|{appointment['description']}\n")

    def load(self) -> None:
        try:
            with open('appointments.txt', 'r') as f:
                for line in f:
                    date, time, description = line.strip().split('|')
                    self.appointments.append({'date': date, 'time': time, 'description': description})
        except FileNotFoundError:
            pass