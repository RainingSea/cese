class EventManager:
    def __init__(self):
        self.events = self.load_events()

    def load_events(self):
        events = {}
        with open('events.txt', 'r') as file:
            for line in file:
                event_id, name, significance, history, location = line.strip().split('|')
                events[event_id] = {
                    'name': name,
                    'significance': significance,
                    'history': history,
                    'location': location
                }
        return events

    def get_events(self) -> list:
        return list(self.events.values())

    def get_event_details(self, event_id: str) -> dict:
        return self.events.get(event_id)

    def search_events(self, query: str) -> list:
        return [event for event in self.events.values() if query.lower() in event['name'].lower()]