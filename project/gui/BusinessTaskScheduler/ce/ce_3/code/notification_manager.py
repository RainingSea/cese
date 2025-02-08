import json
from typing import List
from datetime import datetime

class Notification:
    def __init__(self, message: str, timestamp: str):
        self.message = message
        self.timestamp = timestamp

class NotificationManager:
    def __init__(self):
        self.notifications = []

    def load_notifications(self) -> None:
        try:
            with open('notifications.txt', 'r') as file:
                self.notifications = [Notification(*line.strip().split('|')) for line in file.readlines()]
        except FileNotFoundError:
            self.notifications = []

    def save_notifications(self) -> None:
        with open('notifications.txt', 'w') as file:
            for notification in self.notifications:
                file.write(f"{notification.message}|{notification.timestamp}\n")

    def add_notification(self, notification: Notification) -> None:
        self.notifications.append(notification)
        self.save_notifications()

    def get_notifications(self) -> List[Notification]:
        return self.notifications