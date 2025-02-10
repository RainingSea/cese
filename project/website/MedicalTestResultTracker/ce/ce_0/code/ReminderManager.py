class Reminder:
    def __init__(self, date: str, message: str):
        self.date = date
        self.message = message

    def save(self):
        with open('reminders.txt', 'a') as f:
            f.write(f"{self.date}|{self.message}\n")

class ReminderManager:
    def add_reminder(self, reminder: Reminder):
        reminder.save()

    def load_reminders(self) -> list:
        try:
            with open('reminders.txt', 'r') as f:
                return f.read().strip().split('\n')
        except FileNotFoundError:
            return []