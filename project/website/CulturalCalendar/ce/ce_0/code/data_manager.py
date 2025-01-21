import json
from typing import List

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> None:
        DataManager.save_user(self)

class Event:
    def __init__(self, title: str, date: str, description: str, location: str):
        self.title = title
        self.date = date
        self.description = description
        self.location = location

    def save(self) -> None:
        DataManager.save_event(self)

class Reminder:
    def __init__(self, user: str, event_title: str):
        self.user = user
        self.event_title = event_title

    def save(self) -> None:
        DataManager.save_reminder(self)

class DataManager:
    @staticmethod
    def load_users() -> List[User]:
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    @staticmethod
    def load_events() -> List[Event]:
        events = []
        try:
            with open('events.txt', 'r') as file:
                for line in file:
                    title, date, description, location = line.strip().split('|')
                    events.append(Event(title, date, description, location))
        except FileNotFoundError:
            pass
        return events

    @staticmethod
    def load_reminders() -> List[Reminder]:
        reminders = []
        try:
            with open('reminders.txt', 'r') as file:
                for line in file:
                    user, event_title = line.strip().split('|')
                    reminders.append(Reminder(user, event_title))
        except FileNotFoundError:
            pass
        return reminders

    @staticmethod
    def save_user(user: User) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{user.username}|{user.password}\n")

    @staticmethod
    def save_event(event: Event) -> None:
        with open('events.txt', 'a') as file:
            file.write(f"{event.title}|{event.date}|{event.description}|{event.location}\n")

    @staticmethod
    def save_reminder(reminder: Reminder) -> None:
        with open('reminders.txt', 'a') as file:
            file.write(f"{reminder.user}|{reminder.event_title}\n")