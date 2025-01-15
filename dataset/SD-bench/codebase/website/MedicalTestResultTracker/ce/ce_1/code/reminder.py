class Reminder:
    def __init__(self, user_id: str, test_name: str, reminder_date: str):
        self.user_id = user_id
        self.test_name = test_name
        self.reminder_date = reminder_date

    def save(self):
        with open('reminders.txt', 'a') as f:
            f.write(f"{self.user_id}|{self.test_name}|{self.reminder_date}\n")

    @staticmethod
    def load_reminders(user_id: str):
        reminders = []
        try:
            with open('reminders.txt', 'r') as f:
                for line in f:
                    uid, test_name, reminder_date = line.strip().split('|')
                    if uid == user_id:
                        reminders.append(Reminder(uid, test_name, reminder_date))
        except FileNotFoundError:
            pass
        return reminders