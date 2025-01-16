import json
from resource import Resource

class ResourceManager:
    def __init__(self):
        self.resources_file = 'resources.json'
        self.resources = self.load_resources()

    def load_resources(self):
        try:
            with open(self.resources_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_resources(self):
        with open(self.resources_file, 'w') as file:
            json.dump(self.resources, file)

    def add_resource(self, title, link, description):
        resource = Resource(title, link, description)
        self.resources.append(resource.__dict__)
        self.save_resources()

    def get_resource(self, resource_id):
        if 0 <= resource_id < len(self.resources):
            return self.resources[resource_id]
        return None