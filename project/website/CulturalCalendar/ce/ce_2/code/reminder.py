class Reminder:
    def __init__(self, user: str, event_title: str):
        self.user = user
        self.event_title = event_title

    def save(self) -> None:
        with open('reminders.txt', 'a') as f:
            f.write(f"{self.user}|{self.event_title}\n")

    @staticmethod
    def load(user: str) -> list:
        reminders = []
        with open('reminders.txt', 'r') as f:
            for line in f:
                reminder_data = line.strip().split('|')
                if reminder_data[0] == user:
                    reminders.append(Reminder(reminder_data[0], reminder_data[1]))
        return reminders