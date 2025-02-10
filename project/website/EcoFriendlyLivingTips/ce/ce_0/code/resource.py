class Resource:
    def __init__(self, url: str, description: str):
        self.url = url
        self.description = description

    def save(self):
        with open('resources.txt', 'a') as f:
            f.write(f"{self.url}|{self.description}\n")

    @staticmethod
    def load_resources() -> list:
        resources = []
        try:
            with open('resources.txt', 'r') as f:
                for line in f:
                    url, description = line.strip().split('|')
                    resources.append(Resource(url, description))
        except FileNotFoundError:
            pass
        return resources