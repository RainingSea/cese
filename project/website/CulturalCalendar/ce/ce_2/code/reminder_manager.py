class ReminderManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.reminders = self.load_reminders()

    def add_reminder(self, user: str, event_id: int) -> bool:
        self.reminders.append({'user': user, 'event_id': event_id})
        self.save_reminders()
        return True

    def load_reminders(self, user: str) -> list:
        reminders = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    reminder_user, event_id = line.strip().split('|')
                    if reminder_user == user:
                        reminders.append(int(event_id))
        except FileNotFoundError:
            pass
        return reminders

    def save_reminders(self):
        with open(self.filename, 'w') as file:
            for reminder in self.reminders:
                file.write(f"{reminder['user']}|{reminder['event_id']}\n")