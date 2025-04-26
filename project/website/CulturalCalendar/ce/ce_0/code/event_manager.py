class EventManager:
    def __init__(self):
        self.events = []

    def load_events(self):
        if os.path.exists('events.txt'):
            with open('events.txt', 'r') as file:
                for line in file:
                    event_details = line.strip().split('|')
                    self.events.append(event_details)

    def get_event_details(self, event_id: str) -> str:
        if int(event_id) < len(self.events):
            event = self.events[int(event_id)]
            return f"Event Name: {event[0]}<br>Significance: {event[1]}<br>History: {event[2]}<br>Location: {event[3]}"
        return "Event not found."