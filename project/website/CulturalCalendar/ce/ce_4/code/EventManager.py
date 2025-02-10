class EventManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.events = self.load_events()

    def load_events(self) -> list:
        events = []
        try:
            with open(self.filepath, 'r') as file:
                for line in file:
                    event_id, title, date, description = line.strip().split('|')
                    events.append({
                        'id': event_id,
                        'title': title,
                        'date': date,
                        'description': description
                    })
        except FileNotFoundError:
            pass
        return events

    def get_event_details(self, event_id: str) -> dict:
        for event in self.events:
            if event['id'] == event_id:
                return event
        return {}

    def search_events(self, query: str) -> list:
        return [event for event in self.events if query.lower() in event['title'].lower()]