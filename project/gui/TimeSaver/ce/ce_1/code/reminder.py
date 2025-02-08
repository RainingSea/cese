class Reminder:
    def __init__(self, date_time: str):
        self.date_time = date_time

    def set_reminder(self, date_time: str) -> None:
        self.date_time = date_time

    def get_reminders(self) -> list:
        return [self.date_time]