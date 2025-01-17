import os

class KnowledgeManager:
    def __init__(self):
        self.file_paths = {
            "theories": "theories.txt",
            "concepts": "concepts.txt",
            "experiments": "experiments.txt"
        }

    def add_knowledge(self, category: str, title: str, content: str) -> None:
        if category not in self.file_paths:
            raise ValueError("Invalid category")
        
        with open(self.file_paths[category], 'a') as file:
            file.write(f"{title}|{content}\n")

    def update_knowledge(self, category: str, title: str, new_content: str) -> None:
        if category not in self.file_paths:
            raise ValueError("Invalid category")
        
        entries = self.retrieve_knowledge(category)
        updated = False
        
        with open(self.file_paths[category], 'w') as file:
            for entry in entries:
                if entry.startswith(title):
                    file.write(f"{title}|{new_content}\n")
                    updated = True
                else:
                    file.write(entry + "\n")
        
        if not updated:
            raise ValueError("Title not found for update")

    def retrieve_knowledge(self, category: str) -> list:
        if category not in self.file_paths:
            raise ValueError("Invalid category")
        
        if not os.path.exists(self.file_paths[category]):
            return []
        
        with open(self.file_paths[category], 'r') as file:
            return [line.strip() for line in file.readlines()]