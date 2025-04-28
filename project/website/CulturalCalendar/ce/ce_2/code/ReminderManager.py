class ReminderManager:
    def __init__(self):
        self.reminders = self.load_reminders()

    def load_reminders(self) -> dict:
        reminders = {}
        try:
            with open('reminders.txt', 'r') as file:
                for line in file:
                    username, event_id = line.strip().split('|')
                    if username not in reminders:
                        reminders[username] = []
                    reminders[username].append(int(event_id))
        except FileNotFoundError:
            pass
        return reminders

    def set_reminder(self, username: str, event_id: int) -> bool:
        if username not in self.reminders:
            self.reminders[username] = []
        if event_id not in self.reminders[username]:
            self.reminders[username].append(event_id)
            with open('reminders.txt', 'a') as file:
                file.write(f"{username}|{event_id}\n")
            return True
        return False

    def get_reminders(self, username: str) -> list:
        return self.reminders.get(username, [])