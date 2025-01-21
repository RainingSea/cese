import os

class Reminder:
    def __init__(self, user: str, event_title: str, reminder_date: str):
        self.user = user
        self.event_title = event_title
        self.reminder_date = reminder_date

    def save(self):
        with open('reminders.txt', 'a') as file:
            file.write(f"{self.user}|{self.event_title}|{self.reminder_date}\n")

    @staticmethod
    def load_for_user(user: str) -> list:
        reminders = []
        if os.path.exists('reminders.txt'):
            with open('reminders.txt', 'r') as file:
                for line in file:
                    reminder_user, event_title, reminder_date = line.strip().split('|')
                    if reminder_user == user:
                        reminders.append(Reminder(reminder_user, event_title, reminder_date))
        return reminders