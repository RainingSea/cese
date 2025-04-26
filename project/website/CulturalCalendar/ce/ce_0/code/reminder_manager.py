class ReminderManager:
    def __init__(self):
        self.reminders = self.load_reminders()

    def load_reminders(self):
        reminders = {}
        if os.path.exists('reminders.txt'):
            with open('reminders.txt', 'r') as file:
                for line in file:
                    username, event_name = line.strip().split('|')
                    if username not in reminders:
                        reminders[username] = []
                    reminders[username].append(event_name)
        return reminders

    def set_reminder(self, username: str, event_id: str):
        event_name = self.events[int(event_id)][0]
        if username not in self.reminders:
            self.reminders[username] = []
        self.reminders[username].append(event_name)
        with open('reminders.txt', 'a') as file:
            file.write(f"{username}|{event_name}\n")

    def get_reminders(self, username: str) -> list:
        return self.reminders.get(username, [])