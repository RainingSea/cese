class ReminderManager:
    def __init__(self, reminders_file: str):
        self.reminders_file = reminders_file
        self.reminders = self.load_reminders()

    def load_reminders(self) -> dict:
        reminders = {}
        try:
            with open(self.reminders_file, 'r') as file:
                for line in file:
                    username, reminder = line.strip().split('|')
                    if username not in reminders:
                        reminders[username] = []
                    reminders[username].append(reminder)
        except FileNotFoundError:
            pass  # If the file does not exist, return an empty dictionary
        return reminders

    def set_reminder(self, username: str, reminder: str) -> None:
        if username not in self.reminders:
            self.reminders[username] = []
        self.reminders[username].append(reminder)
        with open(self.reminders_file, 'a') as file:
            file.write(f"{username}|{reminder}\n")

    def get_reminders(self, username: str) -> list:
        return self.reminders.get(username, [])