class Entry:
    def __init__(self):
        self.entries = self.load_entries()

    def load_entries(self):
        entries = []
        try:
            with open('entries.txt', 'r') as file:
                for line in file:
                    destination, date, activities, photos, reflections = line.strip().split('|')
                    entries.append({
                        'destination': destination,
                        'date': date,
                        'activities': activities,
                        'photos': photos,
                        'reflections': reflections
                    })
        except FileNotFoundError:
            pass
        return entries

    def save(self, destination, date, activities, photos, reflections):
        with open('entries.txt', 'a') as file:
            file.write(f"{destination}|{date}|{activities}|{photos}|{reflections}\n")
        self.entries.append({
            'destination': destination,
            'date': date,
            'activities': activities,
            'photos': photos,
            'reflections': reflections
        })