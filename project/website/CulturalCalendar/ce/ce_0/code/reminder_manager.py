class ReminderManager:
    def __init__(self):
        self.reminders = {}
        self.load_reminders()

    def set_reminder(self, user_id: int, event_id: int) -> None:
        if user_id not in self.reminders:
            self.reminders[user_id] = []
        self.reminders[user_id].append(event_id)
        self.save_reminders()

    def load_reminders(self) -> None:
        try:
            with open('reminders.txt', 'r') as file:
                for line in file:
                    user_id, event_id = map(int, line.strip().split('|'))
                    if user_id not in self.reminders:
                        self.reminders[user_id] = []
                    self.reminders[user_id].append(event_id)
        except FileNotFoundError:
            pass

    def save_reminders(self) -> None:
        with open('reminders.txt', 'w') as file:
            for user_id, event_ids in self.reminders.items():
                for event_id in event_ids:
                    file.write(f"{user_id}|{event_id}\n")