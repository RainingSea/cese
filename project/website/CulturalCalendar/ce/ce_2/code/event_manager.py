class EventManager:
    def __init__(self):
        self.events = self.load_events()
        self.reminders = self.load_reminders()

    def load_events(self):
        events = []
        if os.path.exists('events.txt'):
            with open('events.txt', 'r') as file:
                for line in file:
                    title, significance, history, location = line.strip().split('|')
                    events.append({
                        'title': title,
                        'significance': significance,
                        'history': history,
                        'location': location
                    })
        return events

    def get_event_details(self, event_title: str):
        for event in self.events:
            if event['title'] == event_title:
                return event
        return None

    def set_reminder(self, username: str, event_title: str):
        self.reminders.append((username, event_title))
        with open('reminders.txt', 'a') as file:
            file.write(f"{username}|{event_title}\n")

    def load_reminders(self):
        reminders = []
        if os.path.exists('reminders.txt'):
            with open('reminders.txt', 'r') as file:
                for line in file:
                    username, event_title = line.strip().split('|')
                    reminders.append((username, event_title))
        return reminders

    def get_reminders(self, username: str):
        return [event_title for user, event_title in self.reminders if user == username]