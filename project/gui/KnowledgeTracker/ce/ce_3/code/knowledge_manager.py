import os

class KnowledgeManager:
    def __init__(self):
        self.file_paths = {
            'theories': 'theories.txt',
            'concepts': 'concepts.txt',
            'experiments': 'experiments.txt'
        }
        self._initialize_files()

    def _initialize_files(self):
        for file_path in self.file_paths.values():
            if not os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    pass  # Create the file if it does not exist

    def add_knowledge(self, category: str, knowledge: str) -> None:
        if category not in self.file_paths:
            raise ValueError("Invalid category")
        with open(self.file_paths[category], 'a') as file:
            file.write(knowledge + '\n')

    def view_knowledge(self, category: str) -> list:
        if category not in self.file_paths:
            raise ValueError("Invalid category")
        with open(self.file_paths[category], 'r') as file:
            return file.read().strip().splitlines()

    def update_knowledge(self, category: str, old_knowledge: str, new_knowledge: str) -> None:
        if category not in self.file_paths:
            raise ValueError("Invalid category")
        knowledge_list = self.view_knowledge(category)
        updated_list = [new_knowledge if knowledge == old_knowledge else knowledge for knowledge in knowledge_list]
        with open(self.file_paths[category], 'w') as file:
            for knowledge in updated_list:
                file.write(knowledge + '\n')