class Reminder:
    def __init__(self, username: str, event_name: str):
        self.username = username
        self.event_name = event_name

    def save(self) -> None:
        with open('reminders.txt', 'a') as file:
            file.write(f"{self.username}|{self.event_name}\n")

    @staticmethod
    def load_reminders(username: str) -> list:
        reminders = []
        with open('reminders.txt', 'r') as file:
            for line in file:
                user, event_name = line.strip().split('|')
                if user == username:
                    reminders.append(Reminder(user, event_name))
        return reminders