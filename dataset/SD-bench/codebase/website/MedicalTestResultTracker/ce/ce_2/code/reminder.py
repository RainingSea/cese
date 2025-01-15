class Reminder:
    def __init__(self, user: str, message: str, date: str):
        self.user = user
        self.message = message
        self.date = date

    def save(self):
        with open('reminders.txt', 'a') as file:
            file.write(f"{self.user}|{self.message}|{self.date}\n")

    @staticmethod
    def load(user: str):
        reminders = []
        with open('reminders.txt', 'r') as file:
            for line in file:
                reminder_user, message, date = line.strip().split('|')
                if reminder_user == user:
                    reminders.append(Reminder(reminder_user, message, date))
        return reminders