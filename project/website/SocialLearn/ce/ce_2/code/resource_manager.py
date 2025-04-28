class ResourceManager:
    def __init__(self):
        self.resources = self.load_resources()

    def load_resources(self):
        resources = []
        with open('resources.txt', 'r') as f:
            for line in f:
                resources.append(line.strip())
        return resources

    def share_resource(self, username: str, resource: str) -> bool:
        self.resources.append(resource)
        self.save_resources()
        return True

    def access_resources(self):
        return self.resources

    def save_resources(self):
        with open('resources.txt', 'w') as f:
            for resource in self.resources:
                f.write(f"{resource}\n")