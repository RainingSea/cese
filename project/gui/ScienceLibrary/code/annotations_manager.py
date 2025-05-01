import json

class AnnotationsManager:
    def __init__(self):
        self.annotations = {}

    def load_annotations(self):
        try:
            with open('annotations.json', 'r') as file:
                self.annotations = json.load(file)
        except FileNotFoundError:
            self.annotations = {}

    def add_annotation(self, article: str, note: str) -> None:
        if article not in self.annotations:
            self.annotations[article] = []
        self.annotations[article].append(note)
        self.save_annotations()

    def get_annotations(self, article: str) -> list:
        return self.annotations.get(article, [])

    def save_annotations(self) -> None:
        with open('annotations.json', 'w') as file:
            json.dump(self.annotations, file, indent=4)