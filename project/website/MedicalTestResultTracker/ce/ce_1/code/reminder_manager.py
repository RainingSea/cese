class ReminderManager:
    def __init__(self):
        self.reminders = self.load_reminders()

    def load_reminders(self):
        reminders = []
        try:
            with open('reminders.txt', 'r') as file:
                for line in file:
                    username, reminder_text, date_time = line.strip().split('|')
                    reminders.append((username, reminder_text, date_time))
        except FileNotFoundError:
            pass
        return reminders

    def set_reminder(self, username: str, reminder_text: str, date_time: str) -> None:
        self.reminders.append((username, reminder_text, date_time))
        with open('reminders.txt', 'a') as file:
            file.write(f"{username}|{reminder_text}|{date_time}\n")

    def get_reminders(self, username: str) -> list:
        return [reminder for reminder in self.reminders if reminder[0] == username]