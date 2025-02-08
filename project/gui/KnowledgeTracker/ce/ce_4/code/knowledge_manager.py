import os

class KnowledgeManager:
    def __init__(self):
        self.knowledge_files = {
            "Theories": "theories.txt",
            "Concepts": "concepts.txt",
            "Experiments": "experiments.txt"
        }
        self._initialize_files()

    def _initialize_files(self):
        for file in self.knowledge_files.values():
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    pass  # Create the file if it doesn't exist

    def add_knowledge(self, category: str, knowledge: str) -> None:
        if category in self.knowledge_files:
            with open(self.knowledge_files[category], 'a') as f:
                f.write(knowledge + '\n')

    def view_knowledge(self, category: str) -> list:
        if category in self.knowledge_files:
            with open(self.knowledge_files[category], 'r') as f:
                return f.readlines()
        return []

    def update_knowledge(self, category: str, old_knowledge: str, new_knowledge: str) -> None:
        if category in self.knowledge_files:
            lines = self.view_knowledge(category)
            with open(self.knowledge_files[category], 'w') as f:
                for line in lines:
                    if line.strip() == old_knowledge:
                        f.write(new_knowledge + '\n')
                    else:
                        f.write(line)