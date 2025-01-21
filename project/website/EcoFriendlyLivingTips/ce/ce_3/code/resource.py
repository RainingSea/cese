class Resource:
    def __init__(self, url: str):
        self.url = url

    def save(self):
        with open('resources.txt', 'a') as file:
            file.write(f"{self.url}\n")

    @staticmethod
    def load_all() -> list:
        resources = []
        with open('resources.txt', 'r') as file:
            for line in file:
                resources.append(Resource(line.strip()))
        return resources