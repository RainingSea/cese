class JournalEntry:
    def __init__(self, username: str, destination: str, dates: str, activities: str, photos: list, reflections: str):
        self.username = username
        self.destination = destination
        self.dates = dates
        self.activities = activities
        self.photos = photos
        self.reflections = reflections

    def save(self) -> None:
        with open('entries.txt', 'a') as file:
            photos_str = ','.join(self.photos)
            file.write(f"{self.username}|{self.destination}|{self.dates}|{self.activities}|{photos_str}|{self.reflections}\n")

    def delete(self) -> None:
        # Placeholder for delete functionality
        pass

    def edit(self) -> None:
        # Placeholder for edit functionality
        pass