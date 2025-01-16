class JournalEntry:
    def __init__(self, destination: str, date: str, activities: str, photos: list, reflections: str):
        self.destination = destination
        self.date = date
        self.activities = activities
        self.photos = photos
        self.reflections = reflections

    def save(self):
        with open('entries.txt', 'a') as f:
            photos_str = ','.join(self.photos)
            f.write(f"{self.destination}|{self.date}|{self.activities}|{photos_str}|{self.reflections}\n")

    @staticmethod
    def load_all() -> list:
        entries = []
        try:
            with open('entries.txt', 'r') as f:
                for line in f:
                    destination, date, activities, photos_str, reflections = line.strip().split('|')
                    photos = photos_str.split(',') if photos_str else []
                    entries.append(JournalEntry(destination, date, activities, photos, reflections))
        except FileNotFoundError:
            pass
        return entries

    def delete(self):
        # This method will be implemented in the future
        pass

    def edit(self, destination: str, date: str, activities: str, photos: list, reflections: str):
        # This method will be implemented in the future
        pass