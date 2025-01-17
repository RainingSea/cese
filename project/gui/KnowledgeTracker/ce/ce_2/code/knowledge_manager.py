import json
from knowledge import Knowledge

class KnowledgeManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.knowledge_list = self.load_knowledge()

    def save_knowledge(self, knowledge: dict):
        self.knowledge_list.append(Knowledge.from_dict(knowledge))
        self._save_to_file()

    def load_knowledge(self) -> list:
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                return [Knowledge.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def update_knowledge(self, index: int, knowledge: dict):
        if 0 <= index < len(self.knowledge_list):
            self.knowledge_list[index] = Knowledge.from_dict(knowledge)
            self._save_to_file()

    def delete_knowledge(self, index: int):
        if 0 <= index < len(self.knowledge_list):
            del self.knowledge_list[index]
            self._save_to_file()

    def _save_to_file(self):
        with open(self.file_path, 'w') as file:
            json.dump([k.to_dict() for k in self.knowledge_list], file)