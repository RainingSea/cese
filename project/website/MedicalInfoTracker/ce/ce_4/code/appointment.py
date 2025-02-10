class Appointment:
    def __init__(self, date: str, time: str, description: str):
        self.date = date
        self.time = time
        self.description = description

    def save(self):
        with open('appointments.txt', 'a') as file:
            file.write(f"{self.username}|{self.date} {self.time} {self.description}\n")