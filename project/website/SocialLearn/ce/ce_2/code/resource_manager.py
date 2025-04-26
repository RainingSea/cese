class ResourceManager:
    def __init__(self):
        self.resources = self.load_resources()

    def load_resources(self):
        resources = []
        with open('resources.txt', 'r') as file:
            for line in file:
                title, link = line.strip().split('|')
                resources.append({'title': title, 'link': link})
        return resources

    def share_resource(self, title: str, link: str) -> bool:
        self.resources.append({'title': title, 'link': link})
        self.save_resources()
        return True

    def get_resources(self):
        return self.resources

    def save_resources(self):
        with open('resources.txt', 'w') as file:
            for resource in self.resources:
                file.write(f"{resource['title']}|{resource['link']}\n")