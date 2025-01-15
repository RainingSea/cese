class Appointment:
    def __init__(self):
        self.reminders = self.load_reminders()

    def load_reminders(self):
        reminders = {}
        try:
            with open('appointments.txt', 'r') as file:
                for line in file:
                    username, date, time = line.strip().split('|')
                    if username not in reminders:
                        reminders[username] = []
                    reminders[username].append({'date': date, 'time': time})
        except FileNotFoundError:
            pass
        return reminders

    def set_reminder(self, username: str, date: str, time: str) -> None:
        if username not in self.reminders:
            self.reminders[username] = []
        self.reminders[username].append({'date': date, 'time': time})
        self.save_reminders()

    def get_reminders(self, username: str) -> list:
        return self.reminders.get(username, [])

    def save_reminders(self):
        with open('appointments.txt', 'w') as file:
            for username, reminders in self.reminders.items():
                for reminder in reminders:
                    file.write(f"{username}|{reminder['date']}|{reminder['time']}\n")