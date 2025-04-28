class ResourceManager:
    def __init__(self):
        self.resources = self.load_resources()

    def load_resources(self):
        resources = []
        try:
            with open('resources.txt', 'r') as file:
                for line in file:
                    title, url = line.strip().split('|')
                    resources.append({'title': title, 'url': url})
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return resources

    def add_resource(self, title: str, url: str) -> bool:
        self.resources.append({'title': title, 'url': url})
        self.save_resources()
        return True

    def get_resources(self) -> list:
        return self.resources

    def save_resources(self):
        with open('resources.txt', 'w') as file:
            for resource in self.resources:
                file.write(f"{resource['title']}|{resource['url']}\n")