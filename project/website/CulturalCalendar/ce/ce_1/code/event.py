class Event:
    def __init__(self, name: str, significance: str, history: str, location: str):
        self.name = name
        self.significance = significance
        self.history = history
        self.location = location

    def save(self) -> None:
        with open('events.txt', 'a') as file:
            file.write(f"{self.name}|{self.significance}|{self.history}|{self.location}\n")

    @staticmethod
    def load_events() -> list:
        events = []
        with open('events.txt', 'r') as file:
            for line in file:
                name, significance, history, location = line.strip().split('|')
                events.append(Event(name, significance, history, location))
        return events