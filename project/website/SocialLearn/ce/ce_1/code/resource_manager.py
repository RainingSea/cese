class ResourceManager:
    def __init__(self):
        self.resources = []

    def share_resource(self, username: str, resource: str) -> None:
        self.resources.append(f"{username}|{resource}")
        self.save_resources()

    def load_resources(self) -> list:
        try:
            with open('resources.txt', 'r') as file:
                self.resources = [line.strip() for line in file]
        except FileNotFoundError:
            self.resources = []

    def save_resources(self) -> None:
        with open('resources.txt', 'w') as file:
            for resource in self.resources:
                file.write(f"{resource}\n")