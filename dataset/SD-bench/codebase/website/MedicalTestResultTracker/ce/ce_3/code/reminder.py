class Reminder:
    def __init__(self, user_id: str, test_name: str, reminder_date: str):
        self.user_id = user_id
        self.test_name = test_name
        self.reminder_date = reminder_date

    def save(self) -> None:
        with open('reminders.txt', 'a') as file:
            file.write(f"{self.user_id}|{self.test_name}|{self.reminder_date}\n")

    @classmethod
    def load_all(cls, user_id: str) -> list:
        reminders = []
        with open('reminders.txt', 'r') as file:
            for line in file:
                uid, test_name, reminder_date = line.strip().split('|')
                if uid == user_id:
                    reminders.append(cls(uid, test_name, reminder_date))
        return reminders