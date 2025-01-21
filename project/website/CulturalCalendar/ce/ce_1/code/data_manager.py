from models import User, Event, Reminder

class DataManager:
    def load_users(self):
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
        return users

    def load_events(self):
        events = []
        with open('events.txt', 'r') as file:
            for line in file:
                title, date, description, location = line.strip().split('|')
                events.append(Event(title, date, description, location))
        return events

    def load_reminders(self):
        reminders = []
        with open('reminders.txt', 'r') as file:
            for line in file:
                user, event_title = line.strip().split('|')
                reminders.append(Reminder(user, event_title))
        return reminders

    def save_user(self, user):
        with open('users.txt', 'a') as file:
            file.write(f"{user.username}|{user.password}\n")

    def save_event(self, event):
        with open('events.txt', 'a') as file:
            file.write(f"{event.title}|{event.date}|{event.description}|{event.location}\n")

    def save_reminder(self, reminder):
        with open('reminders.txt', 'a') as file:
            file.write(f"{reminder.user}|{reminder.event_title}\n")