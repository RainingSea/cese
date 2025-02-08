import os

class NotificationManager:
    def __init__(self):
        self.notifications = []
        self.load_notifications()

    def load_notifications(self) -> None:
        if os.path.exists('notifications.txt'):
            with open('notifications.txt', 'r') as file:
                self.notifications = [line.strip() for line in file]

    def save_notifications(self) -> None:
        with open('notifications.txt', 'w') as file:
            for notification in self.notifications:
                file.write(notification + '\n')

    def add_notification(self, message: str) -> None:
        self.notifications.append(message)
        self.save_notifications()

    def get_notifications(self) -> list[str]:
        return self.notifications