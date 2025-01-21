class Event:
    def __init__(self, title: str, date: str, details: str):
        self.title = title
        self.date = date
        self.details = details

    def save(self):
        with open('events.txt', 'a') as file:
            file.write(f"{self.title}|{self.date}|{self.details}\n")

    @staticmethod
    def load_all():
        events = []
        with open('events.txt', 'r') as file:
            for line in file:
                title, date, details = line.strip().split('|')
                events.append(Event(title, date, details))
        return events