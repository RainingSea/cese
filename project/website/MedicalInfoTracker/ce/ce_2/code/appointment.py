class Appointment:
    def __init__(self, date: str, time: str):
        self.date = date
        self.time = time

    def save(self):
        with open('appointments.txt', 'a') as file:
            file.write(f"{self.date}|{self.time}\n")