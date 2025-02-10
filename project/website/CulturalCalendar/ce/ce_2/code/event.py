class Event:
    def __init__(self, title: str, date: str, details: str):
        self.title = title
        self.date = date
        self.details = details

    def save(self) -> None:
        with open('events.txt', 'a') as f:
            f.write(f"{self.title}|{self.date}|{self.details}\n")

    @staticmethod
    def load_all() -> list:
        events = []
        with open('events.txt', 'r') as f:
            for line in f:
                title, date, details = line.strip().split('|')
                events.append(Event(title, date, details))
        return events