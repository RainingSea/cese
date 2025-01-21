class Resource:
    """Represents an eco-friendly resource."""
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url

    def save(self):
        """Saves the resource to a file."""
        with open('resources.txt', 'a') as file:
            file.write(f"{self.title}|{self.url}\n")

    @staticmethod
    def load_all():
        """Loads all resources from the file."""
        resources = []
        with open('resources.txt', 'r') as file:
            for line in file:
                title, url = line.strip().split('|')
                resources.append(Resource(title, url))
        return resources