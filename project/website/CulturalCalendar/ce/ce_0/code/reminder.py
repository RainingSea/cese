class Reminder:
    def __init__(self):
        self.reminders = self.load_reminders()

    def load_reminders(self):
        reminders = {}
        with open('reminders.txt', 'r') as file:
            for line in file:
                username, event_id = line.strip().split('|')
                if username not in reminders:
                    reminders[username] = []
                reminders[username].append(event_id)
        return reminders

    def add_reminder(self, username: str, event_id: str) -> bool:
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