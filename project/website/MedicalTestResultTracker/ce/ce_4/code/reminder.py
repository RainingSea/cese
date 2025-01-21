class Reminder:
    def __init__(self, user_id: str, test_name: str, date: str):
        self.user_id = user_id
        self.test_name = test_name
        self.date = date

    def save(self) -> None:
        with open('reminders.txt', 'a') as file:
            file.write(f"{self.user_id}|{self.test_name}|{self.date}\n")

    @staticmethod
    def load_all(user_id: str) -> list:
        reminders = []
        with open('reminders.txt', 'r') as file:
            for line in file:
                uid, test_name, date = line.strip().split('|')
                if uid == user_id:
                    reminders.append(Reminder(uid, test_name, date))
        return reminders