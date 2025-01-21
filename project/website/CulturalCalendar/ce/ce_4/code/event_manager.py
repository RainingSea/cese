class EventManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.events = self.load_events()

    def load_events(self) -> list:
        events = []
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    event_id, title, description = line.strip().split('|')
                    events.append({'id': int(event_id), 'title': title, 'description': description})
        except FileNotFoundError:
            pass
        return events

    def get_event_details(self, event_id: int) -> dict:
        for event in self.events:
            if event['id'] == event_id:
                return event
        return {}

    def search_events(self, query: str) -> list:
        return [event for event in self.events if query.lower() in event['title'].lower()]