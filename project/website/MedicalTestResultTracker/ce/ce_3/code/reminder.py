class Reminder:
    def __init__(self, test_name: str, reminder_date: str):
        self.test_name = test_name
        self.reminder_date = reminder_date

    def save(self, username: str) -> None:
        with open(f'reminders_{username}.txt', 'a') as f:
            f.write(f"{self.test_name}|{self.reminder_date}\n")

    @staticmethod
    def load(username: str) -> list:
        reminders = []
        try:
            with open(f'reminders_{username}.txt', 'r') as f:
                for line in f:
                    reminder_data = line.strip().split('|')
                    reminders.append({
                        'test_name': reminder_data[0],
                        'reminder_date': reminder_data[1]
                    })
        except FileNotFoundError:
            return reminders
        return reminders