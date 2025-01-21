class ReminderManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.reminders = self.load_reminders()

    def add_reminder(self, username: str, event_id: int) -> bool:
        self.reminders.append({'username': username, 'event_id': event_id})
        self.save_reminders()
        return True

    def load_reminders(self, username: str) -> list:
        reminders = []
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    user, event_id = line.strip().split('|')
                    if user == username:
                        reminders.append(int(event_id))
        except FileNotFoundError:
            pass
        return reminders

    def save_reminders(self):
        with open(self.file_path, 'w') as file:
            for reminder in self.reminders:
                file.write(f"{reminder['username']}|{reminder['event_id']}\n")