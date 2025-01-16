class Reminder:
    def __init__(self, user: str, message: str, date: str):
        self.user = user
        self.message = message
        self.date = date

    def save_to_file(self, filename: str):
        with open(filename, 'a') as file:
            file.write(f"{self.user}|{self.message}|{self.date}\n")

    @staticmethod
    def load_from_file(filename: str) -> list:
        reminders = []
        with open(filename, 'r') as file:
            for line in file:
                user, message, date = line.strip().split('|')
                reminders.append(Reminder(user, message, date))
        return reminders