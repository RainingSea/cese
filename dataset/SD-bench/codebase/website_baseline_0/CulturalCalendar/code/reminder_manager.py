import json

class ReminderManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.reminders = self.load_reminders()

    def add_reminder(self, username: str, event_id: int) -> bool:
        if username not in self.reminders:
            self.reminders[username] = []
        self.reminders[username].append(event_id)
        self.save_reminders()
        return True

    def load_reminders(self, username: str) -> list:
        try:
            with open(self.filename, 'r') as file:
                reminders = json.load(file)
                return reminders.get(username, [])
        except FileNotFoundError:
            return []

    def save_reminders(self):
        with open(self.filename, 'w') as file:
            json.dump(self.reminders, file)