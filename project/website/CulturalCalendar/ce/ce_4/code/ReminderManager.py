class ReminderManager:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def add_reminder(self, user: str, event_id: str) -> bool:
        with open(self.filepath, 'a') as file:
            file.write(f"{user}|{event_id}\n")
        return True

    def load_reminders(self, user: str) -> list:
        reminders = []
        try:
            with open(self.filepath, 'r') as file:
                for line in file:
                    reminder_user, event_id = line.strip().split('|')
                    if reminder_user == user:
                        reminders.append(event_id)
        except FileNotFoundError:
            pass
        return reminders