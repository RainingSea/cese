import os

class KnowledgeTracker:
    def __init__(self):
        self.theories = self.retrieve_theories()
        self.concepts = self.retrieve_concepts()
        self.experiments = self.retrieve_experiments()

    def add_theory(self, entry: str) -> None:
        self.theories.append(entry)
        self._save_to_file('theories.txt', self.theories)

    def add_concept(self, entry: str) -> None:
        self.concepts.append(entry)
        self._save_to_file('concepts.txt', self.concepts)

    def add_experiment(self, entry: str) -> None:
        self.experiments.append(entry)
        self._save_to_file('experiments.txt', self.experiments)

    def update_theory(self, index: int, entry: str) -> None:
        if 0 <= index < len(self.theories):
            self.theories[index] = entry
            self._save_to_file('theories.txt', self.theories)

    def update_concept(self, index: int, entry: str) -> None:
        if 0 <= index < len(self.concepts):
            self.concepts[index] = entry
            self._save_to_file('concepts.txt', self.concepts)

    def update_experiment(self, index: int, entry: str) -> None:
        if 0 <= index < len(self.experiments):
            self.experiments[index] = entry
            self._save_to_file('experiments.txt', self.experiments)

    def retrieve_theories(self) -> list:
        return self._load_from_file('theories.txt')

    def retrieve_concepts(self) -> list:
        return self._load_from_file('concepts.txt')

    def retrieve_experiments(self) -> list:
        return self._load_from_file('experiments.txt')

    def _load_from_file(self, filename: str) -> list:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return [line.strip() for line in file.readlines()]
        return []

    def _save_to_file(self, filename: str, data: list) -> None:
        with open(filename, 'w') as file:
            for entry in data:
                file.write(f"{entry}\n")