class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Event:
    def __init__(self, title: str, date: str, description: str, location: str):
        self.title = title
        self.date = date
        self.description = description
        self.location = location

class Reminder:
    def __init__(self, user: str, event_title: str):
        self.user = user
        self.event_title = event_title