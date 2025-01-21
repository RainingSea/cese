import os

class Event:
    def __init__(self, title: str, date: str, description: str):
        self.title = title
        self.date = date
        self.description = description

    def save(self):
        with open('events.txt', 'a') as file:
            file.write(f"{self.title}|{self.date}|{self.description}\n")

    @staticmethod
    def load_all() -> list:
        events = []
        if os.path.exists('events.txt'):
            with open('events.txt', 'r') as file:
                for line in file:
                    title, date, description = line.strip().split('|')
                    events.append(Event(title, date, description))
        return events