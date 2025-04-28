class ReminderManager:
    def __init__(self, reminders_file: str):
        self.reminders_file = reminders_file
        self.load_reminders()

    def load_reminders(self):
        self.reminders = []
        with open(self.reminders_file, 'r') as file:
            for line in file:
                date, time, description = line.strip().split('|')
                self.reminders.append([date, time, description])

    def set_reminder(self, date: str, time: str, description: str):
        self.reminders.append([date, time, description])
        with open(self.reminders_file, 'a') as file:
            file.write(f"{date}|{time}|{description}\n")

    def get_reminders(self):
        return self.reminders