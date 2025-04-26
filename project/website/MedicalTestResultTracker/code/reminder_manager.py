class ReminderManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.reminders = self.load_reminders()

    def set_reminder(self, username: str, reminder_text: str, date_time: str) -> bool:
        if username is None:
            return False
        self.reminders.append(f"{username}|{reminder_text}|{date_time}")
        self.save_reminders()
        return True

    def get_reminders(self, username: str) -> list:
        if username is None:
            return []
        return [reminder.split('|')[1:] for reminder in self.reminders if reminder.startswith(username)]

    def load_reminders(self) -> list:
        try:
            with open(self.filename, 'r') as file:
                return file.read().strip().split('\n')
        except FileNotFoundError:
            return []

    def save_reminders(self):
        with open(self.filename, 'w') as file:
            file.write('\n'.join(self.reminders))