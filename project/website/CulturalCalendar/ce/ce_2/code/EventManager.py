class EventManager:
    def __init__(self):
        self.events = self.load_events()

    def load_events(self) -> list:
        events = []
        try:
            with open('events.txt', 'r') as file:
                for line in file:
                    events.append(line.strip().split('|'))
        except FileNotFoundError:
            pass
        return events

    def search_events(self, query: str) -> list:
        return [event for event in self.events if query.lower() in event[0].lower()]