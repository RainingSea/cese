class Reminder:
    def __init__(self):
        self.reminders = []

    def add_reminder(self, reminder: str) -> None:
        self.reminders.append(reminder)
        self.save_reminders()

    def save_reminders(self) -> None:
        with open('reminders.txt', 'w') as file:
            for reminder in self.reminders:
                file.write(f"{reminder}\n")

    def load_reminders(self) -> None:
        if os.path.exists('reminders.txt'):
            with open('reminders.txt', 'r') as file:
                self.reminders = [line.strip() for line in file]