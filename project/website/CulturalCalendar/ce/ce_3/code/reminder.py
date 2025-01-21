class Reminder:
    def __init__(self, user: str, event_title: str):
        self.user = user
        self.event_title = event_title

    def save(self):
        with open('reminders.txt', 'a') as file:
            file.write(f"{self.user}|{self.event_title}\n")

    @staticmethod
    def load_for_user(user: str):
        reminders = []
        with open('reminders.txt', 'r') as file:
            for line in file:
                reminder_user, event_title = line.strip().split('|')
                if reminder_user == user:
                    reminders.append(Reminder(reminder_user, event_title))
        return reminders