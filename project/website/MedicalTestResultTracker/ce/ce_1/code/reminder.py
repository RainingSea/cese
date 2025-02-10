class Reminder:
    def __init__(self):
        self.reminders_file_template = 'reminders_{}.txt'

    def set_reminder(self, username: str, date: str, description: str) -> None:
        reminders_file = self.reminders_file_template.format(username)
        with open(reminders_file, 'a') as file:
            file.write(f"{date}|{description}\n")

    def get_reminders(self, username: str) -> list:
        reminders_file = self.reminders_file_template.format(username)
        reminders = []
        if os.path.exists(reminders_file):
            with open(reminders_file, 'r') as file:
                for line in file:
                    date, description = line.strip().split('|')
                    reminders.append((date, description))
        return reminders