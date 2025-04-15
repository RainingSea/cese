class Appointment:
    def __init__(self, date: str, time: str, description: str):
        self.date = date
        self.time = time
        self.description = description

    def save(self) -> None:
        with open('appointments.txt', 'a') as file:
            file.write(f"{self.date}|{self.time}|{self.description}\n")

    @staticmethod
    def load_appointments() -> list:
        appointments = []
        try:
            with open('appointments.txt', 'r') as file:
                for line in file:
                    date, time, description = line.strip().split('|')
                    appointments.append(Appointment(date, time, description))
        except FileNotFoundError:
            pass
        return appointments