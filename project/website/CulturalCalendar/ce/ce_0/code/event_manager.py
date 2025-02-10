class EventManager:
    def __init__(self):
        self.events = []
        self.load_events()

    def load_events(self) -> None:
        try:
            with open('events.txt', 'r') as file:
                for line in file:
                    event_details = line.strip().split('|')
                    self.events.append({
                        'id': len(self.events),
                        'title': event_details[0],
                        'date': event_details[1],
                        'description': event_details[2]
                    })
        except FileNotFoundError:
            pass

    def get_event_details(self, event_id: int) -> dict:
        return self.events[event_id] if 0 <= event_id < len(self.events) else {}

    def search_events(self, query: str) -> list:
        return [event for event in self.events if query.lower() in event['title'].lower()]

    def add_event(self, event: dict) -> None:
        self.events.append(event)
        self.save_events()

    def save_events(self) -> None:
        with open('events.txt', 'w') as file:
            for event in self.events:
                file.write(f"{event['title']}|{event['date']}|{event['description']}\n")