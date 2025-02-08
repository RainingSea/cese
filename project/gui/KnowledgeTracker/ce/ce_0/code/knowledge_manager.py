import json
import os

class KnowledgeManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.knowledge_data = self.load_knowledge()

    def load_knowledge(self) -> list:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        return []

    def add_knowledge(self, entry: dict):
        self.knowledge_data.append(entry)
        self.save_knowledge()

    def update_knowledge(self, entry: dict):
        for i, item in enumerate(self.knowledge_data):
            if item['id'] == entry['id']:
                self.knowledge_data[i] = entry
                break
        self.save_knowledge()

    def retrieve_knowledge(self) -> list:
        return self.knowledge_data

    def save_knowledge(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.knowledge_data, file, indent=4)