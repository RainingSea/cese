class Resource:
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url

    def save(self):
        with open('resources.txt', 'a') as file:
            file.write(f"{self.title}|{self.url}\n")

    @staticmethod
    def load_all():
        resources = []
        with open('resources.txt', 'r') as file:
            for line in file:
                title, url = line.strip().split('|')
                resources.append(Resource(title, url))
        return resources