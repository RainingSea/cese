class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")


class JournalEntry:
    def __init__(self, destination: str, dates: str, activities: str, photos: list, reflections: str):
        self.destination = destination
        self.dates = dates
        self.activities = activities
        self.photos = photos
        self.reflections = reflections

    def save(self):
        entry_data = {
            "destination": self.destination,
            "dates": self.dates,
            "activities": self.activities,
            "photos": self.photos,
            "reflections": self.reflections
        }
        with open('entries.txt', 'a') as file:
            file.write(f"{entry_data}\n")

    def to_dict(self):
        return {
            "destination": self.destination,
            "dates": self.dates,
            "activities": self.activities,
            "photos": self.photos,
            "reflections": self.reflections
        }